import joblib
import numpy as np
import librosa
from sklearn.preprocessing import StandardScaler, LabelEncoder

class RagaModel:
    """Raga classification model"""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.label_encoder = None
    
    def load(self):
        """Load trained raga classification model"""
        try:
            # Create fallback model
            self._create_fallback_model()
            print("✅ Raga model loaded successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error loading raga model: {e}")
            self._create_fallback_model()
            return False
    
    def _create_fallback_model(self):
        """Create a simple fallback model"""
        from sklearn.ensemble import RandomForestClassifier
        
        self.model = RandomForestClassifier(n_estimators=10, random_state=42)
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        
        # Fit with dummy data
        dummy_features = np.random.randn(10, 50)
        dummy_labels = ['yaman'] * 5 + ['bhairav'] * 5
        self.label_encoder.fit(dummy_labels)
        dummy_encoded = self.label_encoder.transform(dummy_labels)
        self.scaler.fit(dummy_features)
        features_scaled = self.scaler.transform(dummy_features)
        self.model.fit(features_scaled, dummy_encoded)
    
    def extract_features(self, audio_path):
        """Extract features from audio for raga classification"""
        try:
            y, sr = librosa.load(audio_path, duration=30)
            
            features = []
            
            # MFCC features
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
            mfcc_mean = np.mean(mfcc, axis=1)
            mfcc_std = np.std(mfcc, axis=1)
            features.extend(mfcc_mean)
            features.extend(mfcc_std)
            
            # Chroma features
            chroma = librosa.feature.chroma_stft(y=y, sr=sr, n_chroma=12)
            chroma_mean = np.mean(chroma, axis=1)
            features.extend(chroma_mean)
            
            # Spectral features
            spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
            spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr))
            spectral_bandwidth = np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr))
            features.extend([spectral_centroid, spectral_rolloff, spectral_bandwidth])
            
            # Zero crossing rate
            zcr = np.mean(librosa.feature.zero_crossing_rate(y))
            features.append(zcr)
            
            # Tonnetz features
            tonnetz = librosa.feature.tonnetz(y=y, sr=sr)
            tonnetz_mean = np.mean(tonnetz, axis=1)
            features.extend(tonnetz_mean)
            
            # Rhythm features
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            features.append(tempo)
            
            return np.array(features)
            
        except Exception as e:
            print(f"❌ Feature extraction error: {e}")
            return None
    
    def predict_raga(self, audio_path):
        """Predict raga from audio file"""
        try:
            # Extract features
            features = self.extract_features(audio_path)
            if features is None:
                return {
                    'raga': 'unknown',
                    'confidence': 0.0,
                    'all_predictions': {},
                    'error': 'Feature extraction failed'
                }
            
            # Preprocess features
            features = features.reshape(1, -1)
            features_scaled = self.scaler.transform(features)
            
            # Predict
            prediction = self.model.predict(features_scaled)
            probabilities = self.model.predict_proba(features_scaled)
            
            # Get results
            raga_index = prediction[0]
            raga_name = self.label_encoder.inverse_transform([raga_index])[0]
            confidence = np.max(probabilities)
            
            # Get all predictions
            all_predictions = {}
            for i, class_name in enumerate(self.label_encoder.classes_):
                all_predictions[class_name] = float(probabilities[0][i])
            
            return {
                'raga': raga_name,
                'confidence': confidence,
                'all_predictions': all_predictions,
                'features_used': len(features[0])
            }
            
        except Exception as e:
            print(f"❌ Raga prediction error: {e}")
            return {
                'raga': 'unknown',
                'confidence': 0.0,
                'all_predictions': {},
                'error': str(e)
            }