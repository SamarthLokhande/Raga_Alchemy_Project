import tensorflow as tf
import numpy as np
import cv2
from deepface import DeepFace
import os
from flask import current_app

class EmotionModel:
    """Emotion detection model wrapper"""
    
    def __init__(self):
        self.model = None
        self.model_path = None
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
        """Detect emotion from image with JSON serializable output"""
        try:
            # Analyze emotion using DeepFace
            result = DeepFace.analyze(
                img_path=image_path,
                actions=['emotion'],
                enforce_detection=False,
                detector_backend='opencv',
                silent=True
            )
            
            # Extract dominant emotion
            if isinstance(result, list) and len(result) > 0:
                emotion_data = result[0]
            else:
                emotion_data = result
                
            dominant_emotion = emotion_data.get('dominant_emotion', 'neutral')
            emotion_scores = emotion_data.get('emotion', {})
            
            # Convert numpy values to Python native types for JSON serialization
            processed_emotions = {}
            for emotion, score in emotion_scores.items():
                if hasattr(score, 'item'):  # If it's a numpy type
                    processed_emotions[emotion] = float(score.item())
                else:
                    processed_emotions[emotion] = float(score)
            
            # Calculate confidence
            confidence = processed_emotions.get(dominant_emotion, 0) / 100.0
            
            return {
                'emotion': dominant_emotion,
                'confidence': float(confidence),
                'all_emotions': processed_emotions,
                'face_detected': True,
                'success': True
            }
            
        except Exception as e:
            print(f"❌ Emotion detection error: {e}")
            return {
                'emotion': 'neutral',
                'confidence': 0.0,
                'all_emotions': {},
                'face_detected': False,
                'error': str(e),
                'success': False
            }
    
    def detect_multiple_faces(self, image_path):
        """Detect emotions for multiple faces in image"""
        try:
            results = DeepFace.analyze(
                img_path=image_path,
                actions=['emotion'],
                enforce_detection=False,
                detector_backend='opencv',
                silent=True
            )
            
            emotions = []
            for result in results:
                emotion_scores = result.get('emotion', {})
                
                # Convert numpy values to Python native types
                processed_scores = {}
                for emotion, score in emotion_scores.items():
                    if hasattr(score, 'item'):
                        processed_scores[emotion] = float(score.item())
                    else:
                        processed_scores[emotion] = float(score)
                
                dominant_emotion = result.get('dominant_emotion', 'neutral')
                confidence = processed_scores.get(dominant_emotion, 0) / 100.0
                
                emotion_data = {
                    'emotion': dominant_emotion,
                    'confidence': float(confidence),
                    'all_emotions': processed_scores,
                    'region': result.get('region', {})
                }
                emotions.append(emotion_data)
            
            return emotions
            
        except Exception as e:
            print(f"❌ Multi-face emotion detection error: {e}")
            return []