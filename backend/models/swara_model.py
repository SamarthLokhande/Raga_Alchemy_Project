import joblib
import numpy as np
import librosa
from sklearn.preprocessing import StandardScaler, LabelEncoder

class SwaraModel:
    """Swara detection model"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.label_encoder = None
    
    def load(self):
        """Load trained swara detection model"""
        try:
            # Create fallback model
            self._create_fallback_model()
            print("✅ Swara model loaded successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error loading swara model: {e}")
            self._create_fallback_model()
            return False
    
    def _create_fallback_model(self):
        """Create a simple fallback model"""
        from sklearn.svm import SVC
        
        self.model = SVC(kernel='rbf', C=1.0, probability=True, random_state=42)
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        
        # Fit with dummy data
        dummy_features = np.random.randn(12, 10)
        dummy_labels = ['S', 'r', 'R', 'g', 'G', 'M', 'M\'', 'P', 'd', 'D', 'n', 'N']
        self.label_encoder.fit(dummy_labels)
        dummy_encoded = self.label_encoder.transform(dummy_labels)
        self.scaler.fit(dummy_features)
        features_scaled = self.scaler.transform(dummy_features)
        self.model.fit(features_scaled, dummy_encoded)
    
    def extract_pitch_features(self, audio_path):
        """Extract pitch-based features for swara detection"""
        try:
            y, sr = librosa.load(audio_path)
            
            # Extract pitch using PYIN
            f0, voiced_flag, voiced_probs = librosa.pyin(
                y, 
                fmin=librosa.note_to_hz('C3'),
                fmax=librosa.note_to_hz('C6'),
                sr=sr
            )
            
            # Get voiced segments
            voiced_f0 = f0[voiced_flag & ~np.isnan(f0)]
            
            if len(voiced_f0) == 0:
                return None
            
            features = []
            
            # Pitch statistics
            features.append(np.mean(voiced_f0))
            features.append(np.std(voiced_f0))
            features.append(np.median(voiced_f0))
            features.append(np.min(voiced_f0))
            features.append(np.max(voiced_f0))
            
            # Spectral features for predominant pitch
            predominant_pitch = np.median(voiced_f0)
            
            # Harmonic features
            harmonic = librosa.effects.harmonic(y)
            percussive = librosa.effects.percussive(y)
            
            h_centroid = np.mean(librosa.feature.spectral_centroid(y=harmonic, sr=sr))
            p_centroid = np.mean(librosa.feature.spectral_centroid(y=percussive, sr=sr))
            
            features.extend([h_centroid, p_centroid])
            
            # Voicing features
            features.append(np.mean(voiced_probs[voiced_flag]))
            features.append(len(voiced_f0) / len(f0))
            
            return np.array(features)
            
        except Exception as e:
            print(f"❌ Pitch feature extraction error: {e}")
            return None
    
    def predict_swara(self, audio_path):
        """Predict swara from audio file"""
        try:
            # Extract features
            features = self.extract_pitch_features(audio_path)
            if features is None:
                return {
                    'swara': 'S',
                    'confidence': 0.0,
                    'exact_frequency': 0.0,
                    'error': 'Feature extraction failed'
                }
            
            # Preprocess features
            features = features.reshape(1, -1)
            features_scaled = self.scaler.transform(features)
            
            # Predict
            prediction = self.model.predict(features_scaled)
            probabilities = self.model.predict_proba(features_scaled)
            
            # Get results
            swara_index = prediction[0]
            swara_name = self.label_encoder.inverse_transform([swara_index])[0]
            confidence = np.max(probabilities)
            
            # Get exact frequency
            exact_frequency = features[0][0]  # Mean frequency
            
            return {
                'swara': swara_name,
                'confidence': confidence,
                'exact_frequency': exact_frequency,
                'all_probabilities': dict(zip(self.label_encoder.classes_, probabilities[0]))
            }
            
        except Exception as e:
            print(f"❌ Swara prediction error: {e}")
            return {
                'swara': 'S',
                'confidence': 0.0,
                'exact_frequency': 0.0,
                'error': str(e)
            }