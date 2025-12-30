"""Main Flask application for AI Navigation Assistant."""
from flask import Flask, render_template, jsonify, request, Response
from flask_cors import CORS
import json
import config
from camera_processor import CameraProcessor
from azure_vision import AzureVisionService, AzureFaceService
# from detectron2_vision import Detectron2VisionService  # Optional: keep as fallback
from audio_service import AudioService
import threading
import time

app = Flask(__name__)
CORS(app)

# Initialize services
camera_processor = None
vision_service = None
face_service = None
audio_service = AudioService()

# Processing state
processing_enabled = False
last_analysis = {}
frame_count = 0  # Track frames for rate limiting


def process_frame(frame):
    """Process frame when available."""
    global last_analysis, processing_enabled, frame_count
    
    if not processing_enabled:
        return
    
    if not vision_service:
        print("Warning: Vision service not available, skipping frame processing")
        return
    
    frame_count += 1
    
    try:
        # Get frame bytes
        import cv2
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        frame_bytes = buffer.tobytes()
        
        # Analyze image
        print("[Processing] Analyzing frame...")
        analysis = vision_service.analyze_image(frame_bytes)
        print(f"[Processing] Analysis keys: {list(analysis.keys())}")
        
        # Check for critical errors
        if 'error' in analysis:
            error_code = analysis.get('error_code', 'UNKNOWN')
            if error_code == 'PUBLIC_ACCESS_DISABLED':
                # Only show this message once every 50 frames to avoid spam
                if frame_count % 50 == 0:
                    print("\n" + "="*60)
                    print("❌ CRITICAL ERROR: Azure Computer Vision Public Access Disabled")
                    print("="*60)
                    print("Your Azure Computer Vision resource has public access disabled.")
                    print("To fix: Azure Portal → Your Resource → Networking → Enable Public Access")
                    print("See AZURE_FIX_GUIDE.md for detailed instructions")
                    print("="*60 + "\n")
            elif error_code == 'RATE_LIMIT':
                if frame_count % 10 == 0:
                    print(f"[Processing] Rate limit hit. Waiting before next analysis...")
                return
            # Don't process further if there's an error
            last_analysis = analysis
            return
        
        # Extract text if needed (only if analysis succeeded)
        text_result = vision_service.read_text(frame_bytes)
        if text_result.get('text'):
            analysis['text'] = text_result['text']
            print(f"[Processing] Text extracted: {text_result['text'][:50]}...")
        
        # Detect faces (only every 10 frames to reduce API calls)
        if face_service and face_service.client:
            if frame_count % 10 == 0:  # Only every 10th frame
                try:
                    faces = face_service.detect_faces(frame_bytes)
                    if faces:
                        analysis['faces'] = faces
                        print(f"[Processing] Faces detected: {len(faces)}")
                except Exception as face_error:
                    # Silently skip - face detection is optional
                    pass
        
        last_analysis = analysis
        
        # Generate audio feedback (only if no errors)
        print("[Processing] Generating audio feedback...")
        generate_audio_feedback(analysis)
        
    except Exception as e:
        print(f"Frame processing error: {e}")
        import traceback
        traceback.print_exc()


def generate_audio_feedback(analysis: dict):
    """Generate audio feedback from analysis results."""
    if not analysis or 'error' in analysis:
        print(f"[Audio] Skipping feedback - analysis error or empty: {analysis}")
        return
    
    print(f"[Audio] Generating feedback for analysis: {list(analysis.keys())}")
    
    # Priority 1: Obstacle warnings
    if analysis.get('obstacles') and len(analysis.get('obstacles', [])) > 0:
        print(f"[Audio] Obstacles detected: {len(analysis['obstacles'])}")
        audio_service.speak_obstacle_warning(analysis['obstacles'])
        # Continue to also speak objects after obstacle warning
    
    # Priority 2: Always speak detected objects
    objects = analysis.get('objects', [])
    if objects and len(objects) > 0:
        # Filter objects by confidence threshold and sort by confidence
        detected_objects = [obj for obj in objects if obj.get('confidence', 0) >= config.Config.OBSTACLE_DETECTION_THRESHOLD]
        detected_objects.sort(key=lambda x: x.get('confidence', 0), reverse=True)
        
        if detected_objects:
            # Limit to top 5 objects to avoid overwhelming audio
            top_objects = detected_objects[:5]
            object_names = [obj.get('name', 'object') for obj in top_objects]
            
            # Format the objects text
            if len(object_names) == 1:
                objects_text = f"Detected {object_names[0]}"
            elif len(object_names) == 2:
                objects_text = f"Detected {object_names[0]} and {object_names[1]}"
            else:
                objects_text = f"Detected {', '.join(object_names[:-1])}, and {object_names[-1]}"
            
            # Add count if there are more objects
            if len(detected_objects) > 5:
                objects_text += f", and {len(detected_objects) - 5} more objects"
            
            print(f"[Audio] Speaking objects: {objects_text}")
            audio_service.speak(objects_text, priority=6)
    
    # Priority 3: Scene description (after objects)
    description = analysis.get('description', '')
    if description and description.strip():
        print(f"[Audio] Speaking description: {description[:50]}...")
        audio_service.speak(description, priority=5)
    
    # Priority 4: Text content
    if analysis.get('text') and analysis['text'].strip():
        text = analysis['text'][:200]  # Limit length
        print(f"[Audio] Speaking text: {text[:50]}...")
        audio_service.speak(f"Text detected: {text}", priority=2)
    
    # Priority 5: Tags (if no description)
    if not description and analysis.get('tags') and len(analysis.get('tags', [])) > 0:
        tags = analysis['tags'][:5]
        tags_text = f"Scene contains: {', '.join(tags)}"
        print(f"[Audio] Speaking tags: {tags_text}")
        audio_service.speak(tags_text, priority=4)
    
    # Priority 6: Faces
    if analysis.get('faces') and len(analysis.get('faces', [])) > 0:
        faces = analysis['faces']
        face_text = f"Detected {len(faces)} face"
        if len(faces) > 1:
            face_text += "s"
        print(f"[Audio] Speaking faces: {face_text}")
        audio_service.speak(face_text, priority=1)


@app.route('/')
def index():
    """Serve main page."""
    return render_template('index.html')


@app.route('/api/camera/start', methods=['POST'])
def start_camera():
    """Start camera capture."""
    global camera_processor, processing_enabled
    
    try:
        camera_index = request.json.get('camera_index', 0) if request.json else 0
        
        if camera_processor:
            camera_processor.stop()
        
        camera_processor = CameraProcessor(camera_index)
        if camera_processor.start():
            camera_processor.add_callback(process_frame)
            processing_enabled = True
            return jsonify({'success': True, 'message': 'Camera started'})
        else:
            return jsonify({'success': False, 'message': 'Failed to start camera'}), 400
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/camera/stop', methods=['POST'])
def stop_camera():
    """Stop camera capture."""
    global camera_processor, processing_enabled
    
    try:
        if camera_processor:
            camera_processor.stop()
            camera_processor = None
        processing_enabled = False
        return jsonify({'success': True, 'message': 'Camera stopped'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/api/camera/frame', methods=['GET'])
def get_frame():
    """Get current camera frame."""
    global camera_processor
    
    if not camera_processor or not camera_processor.is_available():
        return jsonify({'error': 'Camera not available'}), 404
    
    frame_base64 = camera_processor.get_frame_base64()
    if frame_base64:
        return jsonify({'frame': frame_base64})
    else:
        return jsonify({'error': 'No frame available'}), 404


@app.route('/api/analysis', methods=['GET'])
def get_analysis():
    """Get latest analysis results."""
    return jsonify(last_analysis)


@app.route('/api/process', methods=['POST'])
def process_image():
    """Process uploaded image."""
    global vision_service, face_service
    
    if not vision_service:
        return jsonify({'error': 'Vision service not available'}), 503
    
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400
        
        image_file = request.files['image']
        image_bytes = image_file.read()
        
        if len(image_bytes) == 0:
            return jsonify({'error': 'Empty image file'}), 400
        
        # Analyze image
        analysis = vision_service.analyze_image(image_bytes)
        
        # Check for errors
        if 'error' in analysis:
            return jsonify(analysis)
        
        # Extract text
        text_result = vision_service.read_text(image_bytes)
        if text_result.get('text'):
            analysis['text'] = text_result['text']
        
        # Detect faces (less frequently to avoid rate limits)
        import random
        if face_service and face_service.client and random.random() < 0.1:  # 10% chance
            try:
                faces = face_service.detect_faces(image_bytes)
                if faces:
                    analysis['faces'] = faces
            except:
                pass  # Silently skip face detection errors
        
        # Note: Audio feedback is now handled on client side for mobile devices
        # Only generate server-side audio if explicitly requested
        # generate_audio_feedback(analysis)  # Commented out - client handles it
        
        return jsonify(analysis)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/audio/speak', methods=['POST'])
def speak_text():
    """Speak text."""
    try:
        data = request.json
        text = data.get('text', '')
        priority = data.get('priority', 0)
        interrupt = data.get('interrupt', False)
        
        if text:
            print(f"[API] Speaking text: {text}")
            audio_service.speak(text, priority, interrupt)
            return jsonify({'success': True, 'message': f'Speaking: {text[:50]}...'})
        else:
            return jsonify({'error': 'No text provided'}), 400
            
    except Exception as e:
        print(f"[API] Speak error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/audio/test', methods=['GET'])
def test_audio():
    """Test audio service."""
    try:
        test_text = "Audio test. If you can hear this, the audio service is working correctly."
        print(f"[API] Testing audio with: {test_text}")
        audio_service.speak(test_text, priority=10, interrupt=True)
        return jsonify({'success': True, 'message': 'Audio test triggered'})
    except Exception as e:
        print(f"[API] Audio test error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get application status."""
    global camera_processor, vision_service, face_service
    
    status = {
        'camera_active': camera_processor is not None and camera_processor.is_available(),
        'vision_service_ready': vision_service is not None,
        'face_service_ready': face_service is not None and face_service.client is not None,
        'processing_enabled': processing_enabled,
        'port': config.Config.PORT
    }
    
    return jsonify(status)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'services': {
            'vision': vision_service is not None,
            'face': face_service is not None and face_service.client is not None,
            'audio': audio_service is not None
        }
    })


def initialize_services():
    """Initialize Azure services."""
    global vision_service, face_service
    
    try:
        vision_service = AzureVisionService()
        print("Azure Computer Vision service initialized")
    except Exception as e:
        print(f"Failed to initialize Vision service: {e}")
        vision_service = None
    
    try:
        face_service = AzureFaceService()
        if face_service.client:
            print("Azure Face service initialized")
        else:
            print("Azure Face service not available (optional)")
    except Exception as e:
        print(f"Face service initialization error: {e}")
        face_service = None


if __name__ == '__main__':
    print("Initializing AI Navigation Assistant...")
    initialize_services()
    
    if not vision_service:
        print("WARNING: Azure Computer Vision service not initialized.")
        print("Please configure AZURE_COMPUTER_VISION_ENDPOINT and AZURE_COMPUTER_VISION_KEY in .env file")
    
    # Check if SSL certificates exist
    import os
    ssl_context = None
    if os.path.exists('cert.pem') and os.path.exists('key.pem'):
        ssl_context = ('cert.pem', 'key.pem')
        print(f"🔒 SSL certificates found - Starting HTTPS server on port {config.Config.PORT}")
        print(f"   Access via: https://192.168.1.45:{config.Config.PORT}/")
    else:
        print(f"🌐 Starting HTTP server on port {config.Config.PORT}")
        print(f"   Access via: http://192.168.1.45:{config.Config.PORT}/")
        print(f"   Note: For mobile camera, HTTPS is required. See setup_ssl.sh or use ngrok")
    
    app.run(host='0.0.0.0', port=config.Config.PORT, ssl_context=ssl_context, debug=config.Config.DEBUG)

