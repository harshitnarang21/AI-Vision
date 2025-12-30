"""Configuration settings for the AI Navigation Assistant."""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration."""
    
    # Detectron2 Model Configuration
    DETECTRON2_MODEL = os.getenv(
        'DETECTRON2_MODEL',
        'COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml'  # Default model
    )
    
    # Azure Computer Vision (optional - for fallback)
    AZURE_COMPUTER_VISION_ENDPOINT = os.getenv(
        'AZURE_COMPUTER_VISION_ENDPOINT',
        'https://your-resource-name.cognitiveservices.azure.com/'
    )
    AZURE_COMPUTER_VISION_KEY = os.getenv('AZURE_COMPUTER_VISION_KEY', '')
    
    # Azure Face API (optional)
    AZURE_FACE_ENDPOINT = os.getenv(
        'AZURE_FACE_ENDPOINT',
        'https://your-resource-name.cognitiveservices.azure.com/'
    )
    AZURE_FACE_KEY = os.getenv('AZURE_FACE_KEY', '')
    
    # Application settings
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    PORT = int(os.getenv('PORT', 5000))
    
    # Processing settings
    FRAME_RATE = 2  # Process every Nth frame to reduce processing load
    OBSTACLE_DETECTION_THRESHOLD = 0.7  # Confidence threshold for obstacle detection
    MIN_OBJECT_SIZE = 50  # Minimum object size in pixels to report


