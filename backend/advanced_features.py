import numpy as np
import pretty_midi
import librosa
from scipy import signal

class RagaCompositionGenerator:
    def __init__(self):
        self.raga_database = {
            'yaman': {
                'aroha': ['S', 'R', 'G', 'M', 'P', 'D', 'N', 'S\''],
                'avroha': ['S\'', 'N', 'D', 'P', 'M', 'G', 'R', 'S'],
                'vadi': 'G',
                'samvadi': 'N',
                'pakad': ['N', 'R', 'G', 'M', 'G', 'R', 'S']
            },
            'bhairav': {
                'aroha': ['S', 'r', 'G', 'M', 'P', 'd', 'N', 'S\''],
                'avroha': ['S\'', 'N', 'd', 'P', 'M', 'G', 'r', 'S'],
                'vadi': 'd',
                'samvadi': 'r',
                'pakad': ['S', 'r', 'G', 'M', 'P', 'd', 'S']
            },
            'malkauns': {
                'aroha': ['S', 'g', 'M', 'd', 'N', 'S\''],
                'avroha': ['S\'', 'N', 'd', 'M', 'g', 'S'],
                'vadi': 'M',
                'samvadi': 'S',
                'pakad': ['S', 'g', 'M', 'd', 'M', 'g', 'S']
            }
        }
        
    def generate_composition(self, raga_name, length=16):
        """Generate melody sequence for a raga"""
        raga = self.raga_database.get(raga_name, self.raga_database['yaman'])
        aroha = raga['aroha']
        avroha = raga['avroha']
        pakad = raga['pakad']
        
        sequence = []
        
        # Start with pakad
        sequence.extend(pakad)
        
        # Generate remaining sequence
        while len(sequence) < length:
            if np.random.random() < 0.3:  # 30% chance to insert pakad
                sequence.extend(pakad)
            else:
                # Use Markov-like transition
                if np.random.random() < 0.6:  # 60% chance for aroha
                    next_swara = np.random.choice(aroha)
                else:  # 40% chance for avroha
                    next_swara = np.random.choice(avroha)
                
                sequence.append(next_swara)
                
                # Ensure sequence doesn't exceed length
                if len(sequence) >= length:
                    break
        
        return sequence[:length]

class EnhancedMidiGenerator:
    def __init__(self):
        self.swara_to_midi = {
            'S': 60, 'R': 62, 'G': 64, 'M': 65, 'P': 67, 'D': 69, 'N': 71,
            'r': 61, 'g': 63, 'd': 68, 'n': 70, 'M\'': 66, 'S\'': 72
        }
        
    def create_enhanced_midi(self, swara_sequence, raga_name, instrument='sitar', tempo=120):
        """Create enhanced MIDI with Indian classical characteristics"""
        midi = pretty_midi.PrettyMIDI()
        
        # Main melody instrument
        melody_instrument = pretty_midi.Instrument(program=0)  # Acoustic Grand Piano
        
        note_duration = 60 / tempo  # Quarter note duration
        
        current_time = 0
        for swara in swara_sequence:
            if swara in self.swara_to_midi:
                note_number = self.swara_to_midi[swara]
                
                note = pretty_midi.Note(
                    velocity=80,
                    pitch=note_number,
                    start=current_time,
                    end=current_time + note_duration
                )
                melody_instrument.notes.append(note)
                current_time += note_duration
        
        midi.instruments.append(melody_instrument)
        return midi