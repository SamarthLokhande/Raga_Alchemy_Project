# backend/advanced_ml/music_generator.py
import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np

class LSTMMusicGenerator:
    def __init__(self, sequence_length=50):
        self.sequence_length = sequence_length
        self.model = self.build_lstm_model()
    
    def build_lstm_model(self):
        """LSTM model for music sequence generation"""
        model = models.Sequential([
            layers.LSTM(256, return_sequences=True, 
                       input_shape=(self.sequence_length, 12)),  # 12 swaras
            layers.Dropout(0.3),
            layers.LSTM(128, return_sequences=True),
            layers.Dropout(0.2),
            layers.LSTM(64),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.2),
            layers.Dense(64, activation='relu'),
            layers.Dense(12, activation='softmax')  # 12 possible swaras
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        return model
    
    def train_on_raga_sequences(self, sequences):
        """Train LSTM on raga sequences"""
        X, y = self.prepare_sequences(sequences)
        history = self.model.fit(X, y, epochs=100, batch_size=32, validation_split=0.2)
        return history
    
    def generate_composition(self, seed_sequence, length=100):
        """Generate new composition using trained LSTM"""
        composition = seed_sequence.copy()
        
        for _ in range(length):
            # Get last sequence_length notes
            last_sequence = composition[-self.sequence_length:]
            last_sequence = np.array(last_sequence).reshape(1, self.sequence_length, 12)
            
            # Predict next note
            next_note_probs = self.model.predict(last_sequence, verbose=0)
            next_note = np.argmax(next_note_probs[0])
            
            composition.append(next_note)
        
        return composition