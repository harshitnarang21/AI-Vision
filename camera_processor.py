"""Real-time camera capture and processing pipeline."""
import cv2
import numpy as np
import base64
from typing import Optional, Callable
import threading
import time
import config


class CameraProcessor:
    """Handles camera capture and frame processing."""
    
    def __init__(self, camera_index: int = 0):
        """
        Initialize camera processor.
        
        Args:
            camera_index: Camera device index (0 for default)
        """
        self.camera_index = camera_index
        self.camera = None
        self.is_running = False
        self.current_frame = None
        self.frame_lock = threading.Lock()
        self.frame_count = 0
        self.callbacks = []
    
    def start(self) -> bool:
        """Start camera capture."""
        try:
            self.camera = cv2.VideoCapture(self.camera_index)
            if not self.camera.isOpened():
                return False
            
            # Set camera properties for better quality
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.camera.set(cv2.CAP_PROP_FPS, 30)
            
            self.is_running = True
            
            # Start capture thread
            self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
            self.capture_thread.start()
            
            return True
            
        except Exception as e:
            print(f"Camera initialization error: {e}")
            return False
    
    def stop(self):
        """Stop camera capture."""
        self.is_running = False
        if self.camera:
            self.camera.release()
            self.camera = None
    
    def _capture_loop(self):
        """Internal loop for capturing frames."""
        while self.is_running:
            ret, frame = self.camera.read()
            if ret:
                with self.frame_lock:
                    self.current_frame = frame.copy()
                    self.frame_count += 1
                
                # Process frame if needed
                if self.frame_count % config.Config.FRAME_RATE == 0:
                    self._notify_callbacks(frame)
            
            time.sleep(0.033)  # ~30 FPS
    
    def get_frame(self) -> Optional[np.ndarray]:
        """Get current frame."""
        with self.frame_lock:
            return self.current_frame.copy() if self.current_frame is not None else None
    
    def get_frame_base64(self) -> Optional[str]:
        """Get current frame as base64 encoded JPEG."""
        frame = self.get_frame()
        if frame is None:
            return None
        
        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        frame_bytes = buffer.tobytes()
        return base64.b64encode(frame_bytes).decode('utf-8')
    
    def get_frame_bytes(self) -> Optional[bytes]:
        """Get current frame as JPEG bytes."""
        frame = self.get_frame()
        if frame is None:
            return None
        
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
        return buffer.tobytes()
    
    def add_callback(self, callback: Callable):
        """Add callback function to be called when new frame is available."""
        self.callbacks.append(callback)
    
    def _notify_callbacks(self, frame: np.ndarray):
        """Notify all registered callbacks."""
        for callback in self.callbacks:
            try:
                callback(frame)
            except Exception as e:
                print(f"Callback error: {e}")
    
    def is_available(self) -> bool:
        """Check if camera is available."""
        return self.camera is not None and self.camera.isOpened()


