import tensorflow as tf
import numpy as np
import cv2
from deepface import DeepFace
import os

class EmotionModel:
    """Emotion detection model wrapper"""
    
    def __init__(self):
        self.model = None
        self.emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
    
    def load(self):
        """Load emotion detection model"""
        try:
            # Use DeepFace for emotion detection
            self.model = DeepFace
            print("✅ Emotion model loaded successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error loading emotion model: {e}")
            # Fallback to DeepFace built-in model
            self.model = DeepFace
            return True
    
    def preprocess_image(self, image_path):
        """Preprocess image for emotion detection"""
        try:
            # Read and validate image
            img = cv2.imread(image_path)
            if img is None:
                raise ValueError("Could not read image")
            
            # Basic validation
            if img.size == 0:
                raise ValueError("Empty image")
                
            return img
            
        except Exception as e:
            raise Exception(f"Image preprocessing failed: {str(e)}")
    
    def detect_emotion(self, image_path):
        """Detect emotion from image"""
        try:
            # Preprocess image
            img = self.preprocess_image(image_path)
            
            # Analyze emotion using DeepFace MAINPART
            result = self.model.analyze(
                img_path=image_path,
                actions=['emotion'],
                enforce_detection=False,
                detector_backend='opencv'
            )
            
            # Extract dominant emotion
            if isinstance(result, list) and len(result) > 0:
                emotion_data = result[0]
            else:
                emotion_data = result
                
            dominant_emotion = emotion_data.get('dominant_emotion', 'neutral')
            emotion_scores = emotion_data.get('emotion', {})
            
            # Calculate confidence
            confidence = emotion_scores.get(dominant_emotion, 0) / 100.0
            
            return {
                'emotion': dominant_emotion,
                'confidence': confidence,
                'all_emotions': emotion_scores,
                'face_detected': True
            }
            
        except Exception as e:
            print(f"❌ Emotion detection error: {e}")
            return {
                'emotion': 'neutral',
                'confidence': 0.0,
                'all_emotions': {},
                'face_detected': False,
                'error': str(e)
            }