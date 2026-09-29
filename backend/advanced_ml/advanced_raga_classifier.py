import tensorflow as tf
import numpy as np
import librosa
import os
from tensorflow.keras import layers, models

class AdvancedRagaClassifier:
    def __init__(self):
        self.model = None
        self.ragas = ['yaman', 'bhairav', 'malkauns', 'kafi', 'bhairavi', 
                     'todi', 'asavari', 'khamaj', 'kalyan', 'kedar']
        self.model_path = 'advanced_models/raga_classifier_cnn_lstm.h5'
    
    def build_cnn_lstm_model(self):
        """Advanced CNN + LSTM model for raga classification"""
        model = models.Sequential([
            # Input layer for MFCC features (20 mfccs x time frames)
            layers.Input(shape=(20, 130, 1)),
            
            # CNN layers for feature extraction
            layers.Conv2D(32, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.BatchNormalization(),
            
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.BatchNormalization(),
            
            layers.Conv2D(128, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.BatchNormalization(),
            
            # Reshape for LSTM
            layers.Reshape((16, 128)),
            
            # LSTM layers for temporal patterns
            layers.LSTM(128, return_sequences=True, dropout=0.2),
            layers.LSTM(64, dropout=0.2),
            
            # Dense layers for classification
            layers.Dense(256, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.3),
            
            layers.Dense(len(self.ragas), activation='softmax')
        ])
        
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy', 'precision', 'recall']
        )
        return model
    
    def load_model(self):
        """Load pre-trained model or create new one"""
        try:
            if os.path.exists(self.model_path):
                self.model = tf.keras.models.load_model(self.model_path)
                print("Advanced raga classifier model loaded successfully!")
            else:
                print("No pre-trained model found. Creating new model...")
                self.model = self.build_cnn_lstm_model()
                # You would train the model here in a real scenario
        except Exception as e:
            print(f"Error loading advanced raga model: {e}")
            self.model = self.build_cnn_lstm_model()
    
    def extract_advanced_features(self, audio_path):
        """Extract advanced audio features for ML"""
        try:
            y, sr = librosa.load(audio_path, duration=30)
            
            # Advanced feature set
            mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20, n_fft=2048, hop_length=512)
            chroma = librosa.feature.chroma_stft(y=y, sr=sr, n_fft=2048, hop_length=512)
            spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
            tonnetz = librosa.feature.tonnetz(y=y, sr=sr)
            
            # Ensure consistent shape
            target_frames = 130
            features = []
            
            for feature in [mfccs, chroma, spectral_contrast, tonnetz]:
                if feature.shape[1] < target_frames:
                    # Pad if too short
                    pad_width = target_frames - feature.shape[1]
                    feature = np.pad(feature, ((0, 0), (0, pad_width)), mode='constant')
                else:
                    # Trim if too long
                    feature = feature[:, :target_frames]
                features.append(feature)
            
            # Stack all features
            combined_features = np.vstack(features)
            
            # Reshape for CNN input (channels_last)
            combined_features = combined_features.reshape(1, combined_features.shape[0], combined_features.shape[1], 1)
            
            return combined_features
            
        except Exception as e:
            print(f"Advanced feature extraction error: {e}")
            return None
    
    def predict_raga_advanced(self, audio_path):
        """Advanced raga prediction using CNN+LSTM"""
        try:
            features = self.extract_advanced_features(audio_path)
            if features is None:
                return {"error": "Feature extraction failed"}
            
            prediction = self.model.predict(features)
            raga_index = np.argmax(prediction[0])
            confidence = np.max(prediction[0])
            
            return {
                "raga": self.ragas[raga_index],
                "confidence": float(confidence),
                "all_predictions": {self.ragas[i]: float(pred) for i, pred in enumerate(prediction[0])},
                "model_type": "CNN+LSTM Advanced"
            }
            
        except Exception as e:
            return {"error": f"Advanced prediction failed: {str(e)}"}