import numpy as np
import librosa
import soundfile as sf
import noisereduce as nr
from scipy import signal
import tempfile
import os

class AudioProcessor:
    """Advanced audio processing utilities for Indian classical music"""
    
    def __init__(self, target_sr=22050):
        self.target_sr = target_sr
        self.swara_frequencies = {
            'S': 261.63, 'r': 277.18, 'R': 293.66, 'g': 311.13,
            'G': 329.63, 'M': 349.23, 'M\'': 370.00, 'P': 392.00,
            'd': 415.30, 'D': 440.00, 'n': 466.16, 'N': 493.88
        }
    
    def load_and_preprocess(self, audio_path, duration=30):
        """Load and preprocess audio file"""
        try:
            # Load audio
            y, sr = librosa.load(audio_path, sr=self.target_sr, duration=duration)
            
            # Preprocessing steps
            y = self.remove_noise(y, sr)
            y = self.normalize_audio(y)
            y = self.trim_silence(y)
            
            return y, sr
        except Exception as e:
            raise Exception(f"Audio preprocessing failed: {str(e)}")
    
    def remove_noise(self, y, sr):
        """Remove background noise using spectral gating"""
        try:
            # Use first 500ms to learn noise profile
            noise_sample = y[:int(0.5 * sr)]
            y_denoised = nr.reduce_noise(y=y, sr=sr, y_noise=noise_sample, prop_decrease=0.8)
            return y_denoised
        except:
            return y  # Return original if noise reduction fails
    
    def normalize_audio(self, y):
        """Normalize audio to -1 to 1 range"""
        return librosa.util.normalize(y)
    
    def trim_silence(self, y, top_db=20):
        """Trim leading and trailing silence"""
        y_trimmed, _ = librosa.effects.trim(y, top_db=top_db)
        return y_trimmed
    
    def extract_detailed_pitch(self, y, sr):
        """Extract detailed pitch information using multiple methods"""
        try:
            # Method 1: PYIN for fundamental frequency
            f0_pyin, voiced_flag, voiced_probs = librosa.pyin(
                y, 
                fmin=librosa.note_to_hz('C3'),
                fmax=librosa.note_to_hz('C6'),
                sr=sr,
                frame_length=2048
            )
            
            return {
                'pyin': f0_pyin,
                'voiced_flag': voiced_flag,
                'voiced_probs': voiced_probs
            }
        except Exception as e:
            print(f"❌ Pitch extraction error: {e}")
            return None
    
    def detect_swara_sequence(self, y, sr, threshold=0.8):
        """Detect sequence of swaras from audio"""
        pitch_data = self.extract_detailed_pitch(y, sr)
        if pitch_data is None:
            return []
        
        f0 = pitch_data['pyin']
        voiced_flag = pitch_data['voiced_flag']
        
        swara_sequence = []
        confidence_scores = []
        
        # Process voiced segments
        for i, (pitch, voiced) in enumerate(zip(f0, voiced_flag)):
            if voiced and not np.isnan(pitch):
                swara, confidence = self.frequency_to_swara(pitch)
                if confidence >= threshold:
                    swara_sequence.append(swara)
                    confidence_scores.append(confidence)
        
        return swara_sequence, confidence_scores
    
    def frequency_to_swara(self, frequency):
        """Convert frequency to swara with confidence score"""
        if frequency <= 0:
            return 'S', 0.0
        
        # Find closest swara
        closest_swara = None
        min_distance = float('inf')
        
        for swara, base_freq in self.swara_frequencies.items():
            # Check multiple octaves
            for octave in range(-2, 3):
                freq_octave = base_freq * (2 ** octave)
                distance = abs(frequency - freq_octave)
                
                if distance < min_distance:
                    min_distance = distance
                    closest_swara = swara
        
        # Calculate confidence based on distance (within ±20 cents)
        max_distance = base_freq * (2 ** (20/1200)) - base_freq
        confidence = max(0, 1 - (min_distance / max_distance))
        
        return closest_swara, confidence
    
    def analyze_vibrato(self, y, sr):
        """Analyze vibrato in singing voice"""
        f0, _, _ = librosa.pyin(y, fmin=80, fmax=1000, sr=sr)
        f0_clean = f0[~np.isnan(f0)]
        
        if len(f0_clean) < 10:
            return 0.0
        
        # Calculate rate of pitch variation
        f0_diff = np.diff(f0_clean)
        vibrato_intensity = np.std(f0_diff)
        
        return float(vibrato_intensity)
    
    def create_spectrogram(self, y, sr, save_path=None):
        """Create and save spectrogram"""
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(12, 8))
        
        # Create mel spectrogram
        S = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128)
        S_dB = librosa.power_to_db(S, ref=np.max)
        
        plt.subplot(2, 1, 1)
        librosa.display.specshow(S_dB, sr=sr, x_axis='time', y_axis='mel')
        plt.colorbar(format='%+2.0f dB')
        plt.title('Mel Spectrogram')
        
        # Create chromagram
        plt.subplot(2, 1, 2)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        librosa.display.specshow(chroma, sr=sr, x_axis='time', y_axis='chroma')
        plt.colorbar()
        plt.title('Chromagram')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            plt.close()
        else:
            # Return as base64
            import io
            import base64
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
            buf.seek(0)
            img_str = base64.b64encode(buf.read()).decode('utf-8')
            plt.close()
            return img_str