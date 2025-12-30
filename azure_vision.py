"""Azure Computer Vision integration for object detection, OCR, and scene analysis."""
import io
from typing import List, Dict, Optional
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import (
    VisualFeatureTypes,
    OperationStatusCodes
)
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image
import config


class AzureVisionService:
    """Service for interacting with Azure Computer Vision API."""
    
    def __init__(self):
        """Initialize Azure Computer Vision client."""
        if not config.Config.AZURE_COMPUTER_VISION_KEY:
            raise ValueError("Azure Computer Vision API key not configured")
        
        credentials = CognitiveServicesCredentials(config.Config.AZURE_COMPUTER_VISION_KEY)
        self.client = ComputerVisionClient(
            config.Config.AZURE_COMPUTER_VISION_ENDPOINT,
            credentials
        )
    
    def analyze_image(self, image_bytes: bytes) -> Dict:
        """
        Analyze image for objects, text, and scene description.
        
        Args:
            image_bytes: Image data as bytes
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            # Convert bytes to image stream
            image_stream = io.BytesIO(image_bytes)
            
            # Analyze image with multiple features
            features = [
                VisualFeatureTypes.objects,
                VisualFeatureTypes.description,
                VisualFeatureTypes.tags,
                VisualFeatureTypes.categories
            ]
            
            analysis = self.client.analyze_image_in_stream(
                image_stream,
                visual_features=features
            )
            
            # Extract results
            description = self._extract_description(analysis)
            objects = self._extract_objects(analysis)
            tags = []
            categories = []
            
            try:
                if hasattr(analysis, 'tags') and analysis.tags:
                    tags = [tag.name for tag in analysis.tags if hasattr(tag, 'name')]
            except Exception as e:
                print(f"Error extracting tags: {e}")
            
            try:
                if hasattr(analysis, 'categories') and analysis.categories:
                    categories = [cat.name for cat in analysis.categories if hasattr(cat, 'name')]
            except Exception as e:
                print(f"Error extracting categories: {e}")
            
            result = {
                'description': description,
                'objects': objects,
                'tags': tags,
                'categories': categories,
                'obstacles': self._identify_obstacles(analysis)
            }
            
            print(f"[Azure Vision] Analysis complete - Description: {description[:50]}..., Objects: {len(objects)}, Tags: {len(tags)}")
            
            return result
            
        except Exception as e:
            error_msg = str(e)
            print(f"[Azure Vision] Analysis error: {error_msg}")
            
            # Provide user-friendly error messages
            if '403' in error_msg and 'Public access is disabled' in error_msg:
                return {
                    'error': 'Azure Computer Vision resource has public access disabled. Please enable public network access in Azure Portal.',
                    'error_code': 'PUBLIC_ACCESS_DISABLED',
                    'solution': 'Go to Azure Portal > Your Computer Vision resource > Networking > Enable public network access'
                }
            elif '401' in error_msg or 'Unauthorized' in error_msg:
                return {
                    'error': 'Invalid API key or endpoint. Please check your Azure credentials in .env file.',
                    'error_code': 'AUTH_ERROR'
                }
            elif '429' in error_msg or 'rate limit' in error_msg.lower():
                return {
                    'error': 'API rate limit exceeded. Please wait a moment and try again.',
                    'error_code': 'RATE_LIMIT',
                    'solution': 'Free tier allows 20 calls/minute. Consider upgrading or reducing processing frequency.'
                }
            
            import traceback
            traceback.print_exc()
            return {'error': error_msg, 'error_code': 'UNKNOWN'}
    
    def read_text(self, image_bytes: bytes) -> Dict:
        """
        Extract text from image using OCR.
        
        Args:
            image_bytes: Image data as bytes
            
        Returns:
            Dictionary containing extracted text
        """
        try:
            image_stream = io.BytesIO(image_bytes)
            
            # Use read API for better text extraction
            read_response = self.client.read_in_stream(
                image_stream,
                raw=True
            )
            
            # Get operation ID
            read_operation_location = read_response.headers["Operation-Location"]
            operation_id = read_operation_location.split("/")[-1]
            
            # Wait for operation to complete
            import time
            while True:
                read_result = self.client.get_read_result(operation_id)
                if read_result.status not in ['notStarted', 'running']:
                    break
                time.sleep(0.1)
            
            # Extract text
            text_lines = []
            if read_result.status == OperationStatusCodes.succeeded:
                for text_result in read_result.analyze_result.read_results:
                    for line in text_result.lines:
                        text_lines.append({
                            'text': line.text,
                            'bounding_box': line.bounding_box
                        })
            
            return {
                'text': '\n'.join([line['text'] for line in text_lines]),
                'lines': text_lines
            }
            
        except Exception as e:
            return {'error': str(e), 'text': ''}
    
    def _extract_description(self, analysis) -> str:
        """Extract scene description from analysis."""
        try:
            if hasattr(analysis, 'description') and analysis.description:
                if hasattr(analysis.description, 'captions') and analysis.description.captions:
                    if len(analysis.description.captions) > 0:
                        caption = analysis.description.captions[0]
                        if hasattr(caption, 'text') and caption.text:
                            return caption.text
            return "Unable to describe scene"
        except Exception as e:
            print(f"Error extracting description: {e}")
            return "Unable to describe scene"
    
    def _extract_objects(self, analysis) -> List[Dict]:
        """Extract detected objects with positions."""
        objects = []
        if hasattr(analysis, 'objects') and analysis.objects:
            for obj in analysis.objects:
                objects.append({
                    'name': obj.object_property,
                    'confidence': obj.confidence,
                    'position': {
                        'x': obj.rectangle.x,
                        'y': obj.rectangle.y,
                        'width': obj.rectangle.w,
                        'height': obj.rectangle.h
                    }
                })
        return objects
    
    def _identify_obstacles(self, analysis) -> List[Dict]:
        """Identify potential obstacles in the scene."""
        obstacles = []
        
        # Check for objects that might be obstacles
        if hasattr(analysis, 'objects') and analysis.objects:
            for obj in analysis.objects:
                # Filter objects that are likely obstacles
                obstacle_keywords = ['person', 'vehicle', 'furniture', 'barrier', 'pole', 'post']
                if any(keyword in obj.object_property.lower() for keyword in obstacle_keywords):
                    if obj.confidence >= config.Config.OBSTACLE_DETECTION_THRESHOLD:
                        obstacles.append({
                            'name': obj.object_property,
                            'confidence': obj.confidence,
                            'position': {
                                'x': obj.rectangle.x,
                                'y': obj.rectangle.y,
                                'width': obj.rectangle.w,
                                'height': obj.rectangle.h
                            },
                            'distance_estimate': self._estimate_distance(obj.rectangle)
                        })
        
        return obstacles
    
    def _estimate_distance(self, rectangle) -> str:
        """Estimate distance based on object size (simple heuristic)."""
        # Larger objects in center are likely closer
        area = rectangle.w * rectangle.h
        if area > 50000:
            return "very close"
        elif area > 20000:
            return "close"
        elif area > 5000:
            return "moderate distance"
        else:
            return "far"


class AzureFaceService:
    """Service for face recognition using Azure Face API."""
    
    def __init__(self):
        """Initialize Azure Face API client."""
        if not config.Config.AZURE_FACE_KEY:
            self.client = None
            return
        
        try:
            from azure.cognitiveservices.vision.face import FaceClient
            from azure.cognitiveservices.vision.face.models import DetectionModel
            
            credentials = CognitiveServicesCredentials(config.Config.AZURE_FACE_KEY)
            self.client = FaceClient(
                config.Config.AZURE_FACE_ENDPOINT,
                credentials
            )
            self.detection_model = DetectionModel.detection_03
        except Exception as e:
            print(f"Face API initialization failed: {e}")
            self.client = None
    
    def detect_faces(self, image_bytes: bytes) -> List[Dict]:
        """
        Detect faces in image.
        
        Args:
            image_bytes: Image data as bytes
            
        Returns:
            List of detected faces with positions
        """
        if not self.client:
            return []
        
        try:
            image_stream = io.BytesIO(image_bytes)
            
            # Try with face attributes first
            try:
                detected_faces = self.client.face.detect_with_stream(
                    image_stream,
                    detection_model=self.detection_model,
                    return_face_attributes=['age', 'gender', 'emotion']
                )
            except Exception as attr_error:
                # Fallback: try without emotion attribute (some API versions don't support it)
                print(f"Warning: Could not get emotion attribute: {attr_error}")
                image_stream.seek(0)  # Reset stream
                detected_faces = self.client.face.detect_with_stream(
                    image_stream,
                    detection_model=self.detection_model,
                    return_face_attributes=['age', 'gender']
                )
            
            faces = []
            for face in detected_faces:
                try:
                    face_data = {
                        'position': {
                            'x': face.face_rectangle.left,
                            'y': face.face_rectangle.top,
                            'width': face.face_rectangle.width,
                            'height': face.face_rectangle.height
                        }
                    }
                    
                    # Safely get attributes
                    if hasattr(face, 'face_attributes') and face.face_attributes:
                        if hasattr(face.face_attributes, 'age'):
                            face_data['age'] = face.face_attributes.age
                        if hasattr(face.face_attributes, 'gender'):
                            face_data['gender'] = face.face_attributes.gender
                        if hasattr(face.face_attributes, 'emotion'):
                            face_data['emotion'] = self._get_primary_emotion(face.face_attributes.emotion)
                        else:
                            face_data['emotion'] = 'neutral'
                    else:
                        face_data['age'] = None
                        face_data['gender'] = None
                        face_data['emotion'] = 'neutral'
                    
                    faces.append(face_data)
                except Exception as face_error:
                    print(f"Error processing face: {face_error}")
                    continue
            
            return faces
            
        except Exception as e:
            error_msg = str(e)
            
            # Handle rate limit errors gracefully
            if '429' in error_msg or 'rate limit' in error_msg.lower():
                # Extract wait time if available
                import re
                wait_match = re.search(r'retry after (\d+) seconds', error_msg)
                if wait_match:
                    wait_time = int(wait_match.group(1))
                    print(f"[Face API] Rate limit exceeded. Please wait {wait_time} seconds. Face detection temporarily disabled.")
                else:
                    print(f"[Face API] Rate limit exceeded. Face detection temporarily disabled.")
                # Return empty list - face detection is optional
                return []
            else:
                print(f"Face detection error: {error_msg}")
                # Only print full traceback for non-rate-limit errors
                if '403' not in error_msg and '401' not in error_msg:
                    import traceback
                    traceback.print_exc()
            return []
    
    def _get_primary_emotion(self, emotion) -> str:
        """Get the primary emotion from emotion attributes."""
        if not emotion:
            return "neutral"
        
        emotions = {
            'anger': emotion.anger,
            'contempt': emotion.contempt,
            'disgust': emotion.disgust,
            'fear': emotion.fear,
            'happiness': emotion.happiness,
            'neutral': emotion.neutral,
            'sadness': emotion.sadness,
            'surprise': emotion.surprise
        }
        
        return max(emotions.items(), key=lambda x: x[1])[0]

