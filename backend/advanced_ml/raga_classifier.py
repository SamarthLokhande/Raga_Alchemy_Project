# backend/advanced_ml/raga_classifier.py
import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np

class AdvancedRagaClassifier:
    def __init__(self):
        self.model = self.build_cnn_lstm_model()
        self.ragas = ['yaman', 'bhairav', 'malkauns', 'kafi', 'bhairavi', 
                     'todi', 'asavari', 'khamaj', 'kalyan', 'kedar']
    
    def build_cnn_lstm_model(self):
        """Advanced CNN + LSTM model for raga classification"""
        model = models.Sequential([
            # CNN for feature extraction
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            layers.Conv2D(64, (3, 3), activation='relu'),
            
            # LSTM for temporal patterns
            layers.Reshape((64, 64)),
            layers.LSTM(128, return_sequences=True),
            layers.LSTM(64),
            
            # Dense layers for classification
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(10, activation='softmax')  # 10 ragas
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        return model
    
    def extract_advanced_features(self, audio_path):
        """Extract advanced audio features for ML"""
        y, sr = librosa.load(audio_path)
        
        # Advanced feature set
        features = []
        
        # MFCC with derivatives
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
        mfcc_delta = librosa.feature.delta(mfcc)
        mfcc_delta2 = librosa.feature.delta(mfcc, order=2)
        
        # Spectral features
        spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        
        # Chroma advanced
        chroma_cens = librosa.feature.chroma_cens(y=y, sr=sr)
        chroma_cqt = librosa.feature.chroma_cqt(y=y, sr=sr)
        
        # Combine all features
        features = np.vstack([
            mfcc, mfcc_delta, mfcc_delta2,
            spectral_contrast, spectral_rolloff,
            chroma_cens, chroma_cqt
        ])
        
        return features