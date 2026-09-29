from flask import request, jsonify
import base64
import os
from datetime import datetime
from advanced_features import EnhancedMidiGenerator, RagaCompositionGenerator
from . import midi_bp

@midi_bp.route('/generate-midi', methods=['POST'])
def generate_midi():
    """Generate MIDI file based on raga specifications"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data provided"
            }), 400

        raga_name = data.get('raga', 'yaman')
        length = data.get('length', 16)
        tempo = data.get('tempo', 120)
        instrument = data.get('instrument', 'sitar')

        # Validate inputs
        if length < 8 or length > 64:
            return jsonify({
                "success": False,
                "error": "Length must be between 8 and 64"
            }), 400

        if tempo < 40 or tempo > 200:
            return jsonify({
                "success": False,
                "error": "Tempo must be between 40 and 200 BPM"
            }), 400

        # Generate composition
        composition_generator = RagaCompositionGenerator()
        swara_sequence = composition_generator.generate_composition(raga_name, length)

        # Generate MIDI
        midi_generator = EnhancedMidiGenerator()
        midi = midi_generator.create_enhanced_midi(
            swara_sequence=swara_sequence,
            raga_name=raga_name,
            instrument=instrument,
            tempo=tempo
        )

        # Save MIDI file temporarily
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        midi_filename = f"raga_{raga_name}_{timestamp}.mid"
        midi_path = os.path.join('temp', midi_filename)
        
        os.makedirs('temp', exist_ok=True)
        midi.write(midi_path)

        # Read and encode MIDI file
        with open(midi_path, 'rb') as f:
            midi_data = base64.b64encode(f.read()).decode('utf-8')

        # Clean up temporary file
        os.remove(midi_path)

        return jsonify({
            "success": True,
            "raga": raga_name,
            "swara_sequence": swara_sequence,
            "midi_data": midi_data,
            "filename": midi_filename,
            "composition_info": {
                "length": len(swara_sequence),
                "tempo": tempo,
                "instrument": instrument
            }
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"MIDI generation failed: {str(e)}"
        }), 500