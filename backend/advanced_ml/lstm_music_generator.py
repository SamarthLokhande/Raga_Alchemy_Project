import tensorflow as tf
import numpy as np
from tensorflow.keras import layers, models
import pretty_midi

class LSTMMusicGenerator:
    def __init__(self, sequence_length=50):
        self.sequence_length = sequence_length
        self.model = None
        self.swara_to_int = {
            'S': 0, 'r': 1, 'R': 2, 'g': 3, 'G': 4, 'M': 5,
            'M\'': 6, 'P': 7, 'd': 8, 'D': 9, 'n': 10, 'N': 11
        }
        self.int_to_swara = {v: k for k, v in self.swara_to_int.items()}
        self.model_path = 'advanced_models/lstm_music_generator.h5'
    
    def build_lstm_model(self):
        """Advanced LSTM model for music generation"""
        model = models.Sequential([
            layers.LSTM(512, return_sequences=True, 
                       input_shape=(self.sequence_length, len(self.swara_to_int)),
                       dropout=0.3, recurrent_dropout=0.2),
            layers.BatchNormalization(),
            
            layers.LSTM(256, return_sequences=True, 
                       dropout=0.2, recurrent_dropout=0.1),
            layers.BatchNormalization(),
            
            layers.LSTM(128, dropout=0.1),
            layers.BatchNormalization(),
            
            layers.Dense(256, activation='relu'),
            layers.Dropout(0.3),
            layers.BatchNormalization(),
            
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.2),
            
            layers.Dense(len(self.swara_to_int), activation='softmax')
        ])
        
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        return model
    
    def load_model(self):
        """Load or create LSTM model"""
        try:
            if tf.io.gfile.exists(self.model_path):
                self.model = tf.keras.models.load_model(self.model_path)
                print("LSTM music generator model loaded successfully!")
            else:
                print("Creating new LSTM music generator model...")
                self.model = self.build_lstm_model()
        except Exception as e:
            print(f"Error loading LSTM model: {e}")
            self.model = self.build_lstm_model()
    
    def generate_composition_advanced(self, raga_name, length=100, temperature=1.0):
        """Generate music using advanced LSTM with temperature sampling"""
        try:
            # Start with raga-specific seed sequence
            seed_sequence = self.get_raga_seed_sequence(raga_name)
            composition = seed_sequence.copy()
            
            for _ in range(length):
                # Prepare input sequence
                if len(composition) >= self.sequence_length:
                    input_seq = composition[-self.sequence_length:]
                else:
                    input_seq = composition + [0] * (self.sequence_length - len(composition))
                
                # Convert to one-hot
                input_encoded = tf.keras.utils.to_categorical(
                    input_seq, num_classes=len(self.swara_to_int)
                )
                input_encoded = input_encoded.reshape(1, self.sequence_length, len(self.swara_to_int))
                
                # Predict with temperature
                predictions = self.model.predict(input_encoded, verbose=0)[0]
                predictions = self.apply_temperature(predictions, temperature)
                
                # Sample next note
                next_note = np.random.choice(len(predictions), p=predictions)
                composition.append(next_note)
            
            # Convert back to swaras
            swara_composition = [self.int_to_swara.get(note, 'S') for note in composition]
            
            return {
                "composition": swara_composition,
                "length": len(swara_composition),
                "model_type": "LSTM Advanced",
                "temperature": temperature
            }
            
        except Exception as e:
            return {"error": f"Advanced composition generation failed: {str(e)}"}
    
    def apply_temperature(self, predictions, temperature):
        """Apply temperature for more creative/random sampling"""
        predictions = np.asarray(predictions).astype('float64')
        predictions = np.log(predictions) / temperature
        exp_preds = np.exp(predictions)
        return exp_preds / np.sum(exp_preds)
    
    def get_raga_seed_sequence(self, raga_name):
        """Get raga-specific seed sequences"""
        raga_seeds = {
            'yaman': [0, 2, 4, 5, 7, 9, 11, 0],  # S R G M P D N S
            'bhairav': [0, 1, 4, 5, 7, 8, 11, 0],  # S r G M P d N S
            'malkauns': [0, 3, 5, 8, 10, 0],  # S g M d n S
        }
        return raga_seeds.get(raga_name, [0, 2, 4, 7, 0])  # Default seed