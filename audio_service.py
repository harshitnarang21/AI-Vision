"""Text-to-speech and spatial audio service."""
import pyttsx3
import threading
import queue
from typing import Optional, Dict, List


class AudioService:
    """Handles text-to-speech with spatial audio cues."""
    
    def __init__(self):
        """Initialize audio service."""
        self.engine = pyttsx3.init()
        self.setup_voice()
        self.queue = queue.Queue()
        self.is_speaking = False
        self.audio_thread = None
        self.current_priority = 0
    
    def setup_voice(self):
        """Configure TTS engine settings."""
        # Set speech rate (words per minute)
        self.engine.setProperty('rate', 150)
        
        # Set volume (0.0 to 1.0)
        self.engine.setProperty('volume', 0.9)
        
        # Try to set a more natural voice
        voices = self.engine.getProperty('voices')
        if voices:
            # Prefer female voice if available (often clearer)
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
    
    def speak(self, text: str, priority: int = 0, interrupt: bool = False):
        """
        Add text to speech queue.
        
        Args:
            text: Text to speak
            priority: Priority level (higher = more important)
            interrupt: If True, clear queue and speak immediately
        """
        if interrupt:
            self.queue.queue.clear()
            self.is_speaking = False
        
        self.queue.put((priority, text))
        
        if not self.is_speaking:
            self._start_speaking_thread()
    
    def speak_spatial(self, text: str, position: Dict, priority: int = 0):
        """
        Speak with spatial audio cues based on object position.
        
        Args:
            text: Text to speak
            position: Dictionary with 'x', 'y', 'width', 'height' keys
            priority: Priority level
        """
        # Calculate spatial direction
        direction = self._calculate_direction(position)
        
        # Add direction cue to text
        if direction:
            spatial_text = f"{direction}. {text}"
        else:
            spatial_text = text
        
        self.speak(spatial_text, priority)
    
    def speak_obstacle_warning(self, obstacles: List[Dict]):
        """Speak obstacle warnings with spatial information."""
        if not obstacles:
            return
        
        warnings = []
        for obstacle in obstacles:
            name = obstacle.get('name', 'object')
            distance = obstacle.get('distance_estimate', 'unknown distance')
            position = obstacle.get('position', {})
            
            direction = self._calculate_direction(position)
            warning = f"{direction} {name} at {distance}"
            warnings.append(warning)
        
        warning_text = "Warning. " + ". ".join(warnings)
        self.speak(warning_text, priority=10, interrupt=True)
    
    def _calculate_direction(self, position: Dict) -> Optional[str]:
        """
        Calculate spatial direction from object position.
        
        Args:
            position: Dictionary with 'x', 'y', 'width', 'height'
            
        Returns:
            Direction string (e.g., "ahead", "left", "right")
        """
        if not position or 'x' not in position:
            return None
        
        x = position.get('x', 0)
        width = position.get('width', 0)
        center_x = x + width / 2
        
        # Assume frame width of 1280 (can be made dynamic)
        frame_center = 640
        
        # Calculate relative position
        relative_x = center_x - frame_center
        
        # Determine direction
        if abs(relative_x) < 100:
            return "ahead"
        elif relative_x < -200:
            return "left"
        elif relative_x > 200:
            return "right"
        elif relative_x < 0:
            return "slightly left"
        else:
            return "slightly right"
    
    def _start_speaking_thread(self):
        """Start background thread for speaking."""
        if self.audio_thread is None or not self.audio_thread.is_alive():
            self.audio_thread = threading.Thread(target=self._speaking_loop, daemon=True)
            self.audio_thread.start()
    
    def _speaking_loop(self):
        """Background loop for processing speech queue."""
        while True:
            try:
                priority, text = self.queue.get(timeout=1)
                self.is_speaking = True
                self.current_priority = priority
                
                # Speak the text
                print(f"[Audio] Speaking: {text[:50]}...")  # Debug log
                self.engine.say(text)
                self.engine.runAndWait()
                
                self.is_speaking = False
                
            except queue.Empty:
                break
            except Exception as e:
                print(f"Speech error: {e}")
                import traceback
                traceback.print_exc()
                self.is_speaking = False
    
    def stop(self):
        """Stop audio service."""
        self.queue.queue.clear()
        self.is_speaking = False

