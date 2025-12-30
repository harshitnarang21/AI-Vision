"""Detectron2 integration for object detection, instance segmentation, and scene analysis."""
import io
import cv2
import numpy as np
from typing import List, Dict, Optional
from PIL import Image
import torch
import config

# Try to import Detectron2
try:
    import detectron2
    from detectron2 import model_zoo
    from detectron2.engine import DefaultPredictor
    from detectron2.config import get_cfg
    from detectron2.utils.visualizer import Visualizer
    from detectron2.data import MetadataCatalog
    DETECTRON2_AVAILABLE = True
except ImportError:
    DETECTRON2_AVAILABLE = False
    print("Warning: Detectron2 not installed. Please install it following the guide.")

# Try to import OCR libraries
try:
    import pytesseract
    OCR_AVAILABLE = True
except ImportError:
    try:
        import easyocr
        OCR_AVAILABLE = True
        EASYOCR_AVAILABLE = True
    except ImportError:
        OCR_AVAILABLE = False
        EASYOCR_AVAILABLE = False
        print("Warning: OCR libraries not available. Install pytesseract or easyocr for text extraction.")


class Detectron2VisionService:
    """Service for object detection using Detectron2."""
    
    def __init__(self, model_name: str = "COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"):
        """
        Initialize Detectron2 predictor.
        
        Args:
            model_name: Model configuration name from Detectron2 model zoo
        """
        if not DETECTRON2_AVAILABLE:
            raise ImportError(
                "Detectron2 is not installed. Please install it:\n"
                "pip install 'git+https://github.com/facebookresearch/detectron2.git'"
            )
        
        # Setup configuration
        self.cfg = get_cfg()
        self.cfg.merge_from_file(model_zoo.get_config_file(model_name))
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = config.Config.OBSTACLE_DETECTION_THRESHOLD
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(model_name)
        self.cfg.MODEL.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Initialize predictor
        self.predictor = DefaultPredictor(self.cfg)
        self.metadata = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0] if len(self.cfg.DATASETS.TRAIN) > 0 else "coco_2017_val")
        
        # Initialize OCR if available
        self.ocr_reader = None
        if EASYOCR_AVAILABLE:
            try:
                self.ocr_reader = easyocr.Reader(['en'], gpu=torch.cuda.is_available())
                print("EasyOCR initialized successfully")
            except Exception as e:
                print(f"Failed to initialize EasyOCR: {e}")
                self.ocr_reader = None
        
        print(f"Detectron2 Vision Service initialized (device: {self.cfg.MODEL.DEVICE})")
    
    def analyze_image(self, image_bytes: bytes) -> Dict:
        """
        Analyze image for objects, scene description, and tags.
        
        Args:
            image_bytes: Image data as bytes
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            # Convert bytes to numpy array
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                return {'error': 'Failed to decode image', 'error_code': 'INVALID_IMAGE'}
            
            # Run inference
            outputs = self.predictor(image)
            
            # Extract detected objects
            objects = self._extract_objects(outputs, image.shape)
            
            # Generate scene description from detected objects
            description = self._generate_description(objects)
            
            # Extract tags/categories from detected objects
            tags = self._extract_tags(objects)
            categories = self._extract_categories(objects)
            
            # Identify obstacles
            obstacles = self._identify_obstacles(objects)
            
            result = {
                'description': description,
                'objects': objects,
                'tags': tags,
                'categories': categories,
                'obstacles': obstacles
            }
            
            print(f"[Detectron2] Analysis complete - Description: {description[:50]}..., Objects: {len(objects)}, Tags: {len(tags)}")
            
            return result
            
        except Exception as e:
            error_msg = str(e)
            print(f"[Detectron2] Analysis error: {error_msg}")
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
        if not OCR_AVAILABLE:
            return {'error': 'OCR not available. Install pytesseract or easyocr.', 'text': ''}
        
        try:
            # Convert bytes to numpy array
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if image is None:
                return {'error': 'Failed to decode image', 'text': ''}
            
            text_lines = []
            
            # Use EasyOCR if available (better accuracy)
            if self.ocr_reader:
                results = self.ocr_reader.readtext(image)
                for (bbox, text, confidence) in results:
                    if confidence > 0.5:  # Filter low confidence detections
                        # Convert bbox to format similar to Azure
                        bbox_array = np.array(bbox)
                        x_coords = bbox_array[:, 0]
                        y_coords = bbox_array[:, 1]
                        bounding_box = [
                            float(min(x_coords)),  # x
                            float(min(y_coords)),  # y
                            float(max(x_coords)),  # x + width
                            float(min(y_coords)),  # y
                            float(max(x_coords)),  # x + width
                            float(max(y_coords)),  # y + height
                            float(min(x_coords)),  # x
                            float(max(y_coords))   # y + height
                        ]
                        text_lines.append({
                            'text': text,
                            'bounding_box': bounding_box,
                            'confidence': float(confidence)
                        })
            # Fallback to pytesseract
            elif hasattr(pytesseract, 'image_to_data'):
                # Get detailed data with bounding boxes
                data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
                n_boxes = len(data['text'])
                for i in range(n_boxes):
                    if int(data['conf'][i]) > 0 and data['text'][i].strip():
                        text_lines.append({
                            'text': data['text'][i],
                            'bounding_box': [
                                data['left'][i],
                                data['top'][i],
                                data['left'][i] + data['width'][i],
                                data['top'][i],
                                data['left'][i] + data['width'][i],
                                data['top'][i] + data['height'][i],
                                data['left'][i],
                                data['top'][i] + data['height'][i]
                            ],
                            'confidence': float(data['conf'][i]) / 100.0
                        })
            else:
                # Simple text extraction
                text = pytesseract.image_to_string(image)
                if text.strip():
                    text_lines.append({
                        'text': text.strip(),
                        'bounding_box': None,
                        'confidence': 1.0
                    })
            
            return {
                'text': '\n'.join([line['text'] for line in text_lines]),
                'lines': text_lines
            }
            
        except Exception as e:
            return {'error': str(e), 'text': ''}
    
    def _extract_objects(self, outputs, image_shape: tuple) -> List[Dict]:
        """Extract detected objects with positions."""
        objects = []
        
        instances = outputs["instances"]
        boxes = instances.pred_boxes.tensor.cpu().numpy()
        scores = instances.scores.cpu().numpy()
        classes = instances.pred_classes.cpu().numpy()
        
        height, width = image_shape[:2]
        
        for i in range(len(instances)):
            box = boxes[i]
            score = float(scores[i])
            class_id = int(classes[i])
            class_name = self.metadata.thing_classes[class_id] if class_id < len(self.metadata.thing_classes) else f"class_{class_id}"
            
            # Convert box coordinates (x1, y1, x2, y2) to (x, y, width, height)
            x1, y1, x2, y2 = box
            x = float(x1)
            y = float(y1)
            w = float(x2 - x1)
            h = float(y2 - y1)
            
            # Filter by minimum size
            if w * h < config.Config.MIN_OBJECT_SIZE:
                continue
            
            objects.append({
                'name': class_name,
                'confidence': score,
                'position': {
                    'x': x,
                    'y': y,
                    'width': w,
                    'height': h
                }
            })
        
        return objects
    
    def _generate_description(self, objects: List[Dict]) -> str:
        """Generate scene description from detected objects."""
        if not objects:
            return "No objects detected in the scene"
        
        # Get top objects by confidence
        top_objects = sorted(objects, key=lambda x: x.get('confidence', 0), reverse=True)[:5]
        object_names = [obj.get('name', 'object') for obj in top_objects]
        
        if len(object_names) == 1:
            return f"A scene with a {object_names[0]}"
        elif len(object_names) == 2:
            return f"A scene with a {object_names[0]} and a {object_names[1]}"
        else:
            return f"A scene with {', '.join(object_names[:-1])}, and {object_names[-1]}"
    
    def _extract_tags(self, objects: List[Dict]) -> List[str]:
        """Extract tags from detected objects."""
        tags = []
        seen = set()
        
        for obj in objects:
            name = obj.get('name', '')
            if name and name not in seen:
                tags.append(name)
                seen.add(name)
        
        return tags
    
    def _extract_categories(self, objects: List[Dict]) -> List[str]:
        """Extract categories from detected objects."""
        # COCO categories mapping
        category_mapping = {
            'person': 'people',
            'bicycle': 'vehicles',
            'car': 'vehicles',
            'motorcycle': 'vehicles',
            'airplane': 'vehicles',
            'bus': 'vehicles',
            'train': 'vehicles',
            'truck': 'vehicles',
            'boat': 'vehicles',
            'traffic light': 'infrastructure',
            'fire hydrant': 'infrastructure',
            'stop sign': 'infrastructure',
            'parking meter': 'infrastructure',
            'bench': 'furniture',
            'bird': 'animals',
            'cat': 'animals',
            'dog': 'animals',
            'horse': 'animals',
            'sheep': 'animals',
            'cow': 'animals',
            'elephant': 'animals',
            'bear': 'animals',
            'zebra': 'animals',
            'giraffe': 'animals',
            'backpack': 'accessories',
            'umbrella': 'accessories',
            'handbag': 'accessories',
            'tie': 'accessories',
            'suitcase': 'accessories',
            'frisbee': 'sports',
            'skis': 'sports',
            'snowboard': 'sports',
            'sports ball': 'sports',
            'kite': 'sports',
            'baseball bat': 'sports',
            'baseball glove': 'sports',
            'skateboard': 'sports',
            'surfboard': 'sports',
            'tennis racket': 'sports',
            'bottle': 'food',
            'wine glass': 'food',
            'cup': 'food',
            'fork': 'food',
            'knife': 'food',
            'spoon': 'food',
            'bowl': 'food',
            'banana': 'food',
            'apple': 'food',
            'sandwich': 'food',
            'orange': 'food',
            'broccoli': 'food',
            'carrot': 'food',
            'hot dog': 'food',
            'pizza': 'food',
            'donut': 'food',
            'cake': 'food',
            'chair': 'furniture',
            'couch': 'furniture',
            'potted plant': 'furniture',
            'bed': 'furniture',
            'dining table': 'furniture',
            'toilet': 'furniture',
            'tv': 'electronics',
            'laptop': 'electronics',
            'mouse': 'electronics',
            'remote': 'electronics',
            'keyboard': 'electronics',
            'cell phone': 'electronics',
            'microwave': 'appliances',
            'oven': 'appliances',
            'toaster': 'appliances',
            'sink': 'appliances',
            'refrigerator': 'appliances',
            'book': 'items',
            'clock': 'items',
            'vase': 'items',
            'scissors': 'items',
            'teddy bear': 'items',
            'hair drier': 'items',
            'toothbrush': 'items'
        }
        
        categories = []
        seen = set()
        
        for obj in objects:
            name = obj.get('name', '').lower()
            category = category_mapping.get(name, 'other')
            if category not in seen:
                categories.append(category)
                seen.add(category)
        
        return categories
    
    def _identify_obstacles(self, objects: List[Dict]) -> List[Dict]:
        """Identify potential obstacles in the scene."""
        obstacles = []
        
        # Keywords for objects that are likely obstacles
        obstacle_keywords = ['person', 'vehicle', 'car', 'truck', 'bus', 'motorcycle', 
                           'bicycle', 'chair', 'table', 'bench', 'barrier', 'pole', 
                           'post', 'fence', 'wall', 'door']
        
        for obj in objects:
            name = obj.get('name', '').lower()
            confidence = obj.get('confidence', 0)
            
            if any(keyword in name for keyword in obstacle_keywords):
                if confidence >= config.Config.OBSTACLE_DETECTION_THRESHOLD:
                    position = obj.get('position', {})
                    obstacles.append({
                        'name': obj.get('name'),
                        'confidence': confidence,
                        'position': position,
                        'distance_estimate': self._estimate_distance(position)
                    })
        
        return obstacles
    
    def _estimate_distance(self, position: Dict) -> str:
        """Estimate distance based on object size (simple heuristic)."""
        width = position.get('width', 0)
        height = position.get('height', 0)
        area = width * height
        
        if area > 50000:
            return "very close"
        elif area > 20000:
            return "close"
        elif area > 5000:
            return "moderate distance"
        else:
            return "far"

