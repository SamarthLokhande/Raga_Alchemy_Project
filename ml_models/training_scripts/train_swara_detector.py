import numpy as np
import librosa
import joblib
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import os

class SwaraDataset:
    def __init__(self, audio_dir):
        self.audio_dir = audio_dir
        self.swaras = ['S', 'r', 'R', 'g', 'G', 'M', 'M\'', 'P', 'd', 'D', 'n', 'N']
        
    def extract_pitch_features(self, audio_path):
        """Extract pitch-based features for swara detection"""
        try:
            y, sr = librosa.load(audio_path)
            
            # Extract pitch using PYIN algorithm
            f0, voiced_flag, voiced_probs = librosa.pyin(
                y, 
                fmin=librosa.note_to_hz('C3'),
                fmax=librosa.note_to_hz('C6'),
                sr=sr
            )
            
            # Get voiced segments
            voiced_f0 = f0[voiced_flag]
            
            if len(voiced_f0) == 0:
                return None
                
            features = []
            
            # Pitch statistics
            features.append(np.mean(voiced_f0))
            features.append(np.std(voiced_f0))
            features.append(np.median(voiced_f0))
            
            # Spectral features for the predominant pitch
            if len(voiced_f0) > 0:
                predominant_pitch = np.median(voiced_f0)
                
                # Harmonic features
                harmonic = librosa.effects.harmonic(y)
                percussive = librosa.effects.percussive(y)
                
                h_centroid = np.mean(librosa.feature.spectral_centroid(y=harmonic, sr=sr))
                p_centroid = np.mean(librosa.feature.spectral_centroid(y=percussive, sr=sr))
                
                features.extend([h_centroid, p_centroid])
            
            return np.array(features)
            
        except Exception as e:
            print(f"Error processing {audio_path}: {e}")
            return None
    
    def create_dataset(self):
        """Create training dataset for swara detection"""
        X = []
        y = []
        
        for swara in self.swaras:
            swara_dir = os.path.join(self.audio_dir, swara)
            if os.path.exists(swara_dir):
                for audio_file in os.listdir(swara_dir):
                    if audio_file.endswith(('.wav', '.mp3')):
                        audio_path = os.path.join(swara_dir, audio_file)
                        features = self.extract_pitch_features(audio_path)
                        if features is not None:
                            X.append(features)
                            y.append(swara)
        
        return np.array(X), np.array(y)

class SwaraClassifier:
    def __init__(self):
        self.model = SVC(kernel='rbf', C=10, gamma='scale', probability=True)
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        
    def train(self, X, y):
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        train_score = self.model.score(X_train_scaled, y_train)
        test_score = self.model.score(X_test_scaled, y_test)
        
        print(f"Training Accuracy: {train_score:.4f}")
        print(f"Test Accuracy: {test_score:.4f}")
        
        return train_score, test_score
    
    def save_model(self, model_path):
        """Save the trained model"""
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler,
            'label_encoder': self.label_encoder
        }, model_path)

# Training script
if __name__ == "__main__":
    print("Training Swara Detection Model...")
    
    # Create dataset
    dataset = SwaraDataset('datasets/swara_audio')
    X, y = dataset.create_dataset()
    
    print(f"Dataset shape: {X.shape}")
    print(f"Classes: {np.unique(y)}")
    
    # Train classifier
    classifier = SwaraClassifier()
    train_score, test_score = classifier.train(X, y)
    
    # Save model
    classifier.save_model('models/swara_classifier.joblib')
    print("Model saved successfully!")