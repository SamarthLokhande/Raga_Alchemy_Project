import numpy as np
import librosa
import soundfile as sf
import os
from scipy import signal

class SyntheticRagaData:
    def __init__(self, sample_rate=22050, duration=5):
        self.sample_rate = sample_rate
        self.duration = duration
        self.swara_frequencies = {
            'S': 261.63, 'r': 277.18, 'R': 293.66, 'g': 311.13,
            'G': 329.63, 'M': 349.23, 'M\'': 370.00, 'P': 392.00,
            'd': 415.30, 'D': 440.00, 'n': 466.16, 'N': 493.88
        }
        
    def generate_swara_audio(self, swara, duration=2):
        """Generate synthetic audio for a swara"""
        frequency = self.swara_frequencies[swara]
        
        # Generate time array
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        # Generate sine wave with some harmonics for richness
        fundamental = np.sin(2 * np.pi * frequency * t)
        first_harmonic = 0.3 * np.sin(2 * np.pi * 2 * frequency * t)
        second_harmonic = 0.1 * np.sin(2 * np.pi * 3 * frequency * t)
        
        # Combine waves
        audio = fundamental + first_harmonic + second_harmonic
        
        # Add ADSR envelope
        envelope = self.adsr_envelope(len(audio))
        audio = audio * envelope
        
        # Normalize
        audio = audio / np.max(np.abs(audio))
        
        return audio
    
    def adsr_envelope(self, length, attack=0.1, decay=0.2, sustain=0.6, release=0.1):
        """Create ADSR envelope for natural sound"""
        attack_len = int(length * attack)
        decay_len = int(length * decay)
        sustain_len = int(length * sustain)
        release_len = int(length * release)
        
        envelope = np.zeros(length)
        
        # Attack
        envelope[:attack_len] = np.linspace(0, 1, attack_len)
        
        # Decay
        envelope[attack_len:attack_len+decay_len] = np.linspace(1, 0.7, decay_len)
        
        # Sustain
        envelope[attack_len+decay_len:attack_len+decay_len+sustain_len] = 0.7
        
        # Release
        release_start = attack_len + decay_len + sustain_len
        envelope[release_start:release_start+release_len] = np.linspace(0.7, 0, release_len)
        
        return envelope
    
    def generate_raga_sequence(self, raga_name, num_sequences=10):
        """Generate synthetic raga sequences"""
        raga_sequences = {
            'yaman': ['S', 'R', 'G', 'M', 'P', 'D', 'N', 'S\''],
            'bhairav': ['S', 'r', 'G', 'M', 'P', 'd', 'N', 'S\''],
            'malkauns': ['S', 'g', 'M', 'd', 'N', 'S\''],
            'kafi': ['S', 'R', 'g', 'M', 'P', 'D', 'n', 'S\''],
            'bhairavi': ['S', 'r', 'g', 'M', 'P', 'd', 'n', 'S\''],
            'todi': ['S', 'r', 'g', 'M', 'P', 'd', 'N', 'S\''],
            'asavari': ['S', 'R', 'g', 'M', 'P', 'd', 'n', 'S\''],
            'khamaj': ['S', 'R', 'G', 'M', 'P', 'D', 'N', 'S\''],
            'kalyan': ['S', 'R', 'G', 'M\'', 'P', 'D', 'N', 'S\''],
            'kedar': ['S', 'R', 'G', 'M', 'P', 'D', 'N', 'S\'']
        }
        
        sequences = []
        raga_swaras = raga_sequences.get(raga_name, ['S', 'R', 'G', 'M', 'P', 'D', 'N'])
        
        for _ in range(num_sequences):
            # Generate random sequence following raga rules
            sequence_length = np.random.randint(8, 16)
            sequence = []
            
            for i in range(sequence_length):
                if i == 0:
                    sequence.append('S')
                elif i == sequence_length - 1:
                    sequence.append('S\'')
                else:
                    # Prefer movement in aroha/avroha pattern
                    if np.random.random() < 0.7:
                        sequence.append(np.random.choice(raga_swaras))
                    else:
                        # Occasionally use adjacent swaras for smoothness
                        current_idx = raga_swaras.index(sequence[-1]) if sequence[-1] in raga_swaras else 0
                        next_idx = max(0, min(len(raga_swaras)-1, current_idx + np.random.choice([-1, 1])))
                        sequence.append(raga_swaras[next_idx])
            
            sequences.append(sequence)
        
        return sequences
    
    def create_synthetic_dataset(self, output_dir='datasets/synthetic'):
        """Create complete synthetic dataset for all ragas"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Create swara dataset
        print("Creating swara dataset...")
        swara_dir = os.path.join(output_dir, 'swaras')
        os.makedirs(swara_dir, exist_ok=True)
        
        for swara in self.swara_frequencies.keys():
            swara_audio = self.generate_swara_audio(swara, duration=3)
            output_path = os.path.join(swara_dir, f'{swara}.wav')
            sf.write(output_path, swara_audio, self.sample_rate)
            print(f"Created {swara}.wav")
        
        # Create raga sequences dataset
        print("\nCreating raga sequences...")
        for raga in ['yaman', 'bhairav', 'malkauns', 'kafi', 'bhairavi', 
                    'todi', 'asavari', 'khamaj', 'kalyan', 'kedar']:
            raga_dir = os.path.join(output_dir, 'ragas', raga)
            os.makedirs(raga_dir, exist_ok=True)
            
            sequences = self.generate_raga_sequence(raga, num_sequences=20)
            
            for i, sequence in enumerate(sequences):
                # Combine swaras to create raga audio
                raga_audio = np.array([])
                for swara in sequence:
                    if swara == 'S\'':
                        swara_audio = self.generate_swara_audio('S', duration=0.5)
                        # Shift octave up
                        swara_audio = librosa.effects.pitch_shift(swara_audio, sr=self.sample_rate, n_steps=12)
                    else:
                        swara_audio = self.generate_swara_audio(swara, duration=0.5)
                    
                    raga_audio = np.concatenate([raga_audio, swara_audio])
                
                output_path = os.path.join(raga_dir, f'{raga}_sequence_{i+1}.wav')
                sf.write(output_path, raga_audio, self.sample_rate)
            
            print(f"Created {len(sequences)} sequences for {raga}")

if __name__ == "__main__":
    print("Generating Synthetic Raga Dataset...")
    generator = SyntheticRagaData()
    generator.create_synthetic_dataset()
    print("Synthetic dataset generation completed!")