from flask import request, jsonify
import numpy as np
import os
from datetime import datetime
from utils.file_utils import FileUtils
from utils.audio_processor import AudioProcessor
from backend.models.model_manager import model_manager
from . import swara_bp

@swara_bp.route('/detect-swaras', methods=['POST'])
def detect_swaras():
    """Detect swaras from audio input with detailed analysis"""
    try:
        if 'audio' not in request.files:
            return jsonify({
                "success": False,
                "error": "No audio file provided"
            }), 400

        audio_file = request.files['audio']
        
        # Validate file
        if not FileUtils.allowed_file(audio_file.filename, 'audio'):
            return jsonify({
                "success": False,
                "error": "Invalid file type. Please upload an audio file"
            }), 400

        # Save uploaded file
        try:
            audio_path = FileUtils.save_uploaded_file(audio_file, 'audio')
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 400

        # Get swara model and detect swaras
        swara_model = model_manager.get_swara_model()
        audio_processor = AudioProcessor()

        # Detect individual swaras
        swara_result = swara_model.predict_swara(audio_path)
        
        # Detect swara sequence
        swara_sequence, confidence_scores = audio_processor.detect_swara_sequence(audio_path, 22050)
        
        # Analyze performance
        y, sr = audio_processor.load_and_preprocess(audio_path)
        pitch_data = audio_processor.extract_detailed_pitch(y, sr)
        vibrato = audio_processor.analyze_vibrato(y, sr)

        # Clean up uploaded file
        FileUtils.cleanup_file(audio_path)

        if swara_result.get('error'):
            return jsonify({
                "success": False,
                "error": swara_result['error']
            }), 500

        # Analyze swara sequence for raga characteristics
        sequence_analysis = analyze_swara_sequence(swara_sequence)
        
        # Calculate accuracy metrics
        accuracy_metrics = calculate_swara_accuracy(swara_sequence, confidence_scores)

        return jsonify({
            "success": True,
            "swara_detection": swara_result,
            "sequence_analysis": sequence_analysis,
            "swara_sequence": swara_sequence,
            "confidence_scores": confidence_scores,
            "performance_metrics": {
                "total_swaras_detected": len(swara_sequence),
                "average_confidence": np.mean(confidence_scores) if confidence_scores else 0,
                "pitch_stability": calculate_pitch_stability_from_sequence(swara_sequence),
                "vibrato_intensity": vibrato
            },
            "accuracy_metrics": accuracy_metrics,
            "suggested_ragas": suggest_ragas_from_swaras(swara_sequence)
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Swara detection failed: {str(e)}"
        }), 500

def analyze_swara_sequence(swara_sequence):
    """Analyze swara sequence for patterns and characteristics"""
    if not swara_sequence:
        return {}
    
    # Calculate basic statistics
    unique_swaras = list(set(swara_sequence))
    swara_frequency = {swara: swara_sequence.count(swara) for swara in unique_swaras}
    
    return {
        "total_swaras": len(swara_sequence),
        "unique_swaras": unique_swaras,
        "swara_frequency": swara_frequency,
        "most_common_swara": max(swara_frequency.items(), key=lambda x: x[1])[0] if swara_frequency else None
    }

def calculate_swara_accuracy(sequence, confidence_scores):
    """Calculate accuracy metrics for swara detection"""
    if not sequence:
        return {}
    
    return {
        "average_confidence": np.mean(confidence_scores) if confidence_scores else 0,
        "high_confidence_ratio": len([c for c in confidence_scores if c >= 0.8]) / len(confidence_scores) if confidence_scores else 0
    }

def calculate_pitch_stability_from_sequence(sequence):
    """Calculate pitch stability from swara sequence"""
    if not sequence:
        return 0.0
    
    # Simple stability measure based on swara transitions
    stable_transitions = 0
    total_transitions = len(sequence) - 1
    
    for i in range(total_transitions):
        # Consider transitions to adjacent swaras as stable
        current = sequence[i]
        next_swara = sequence[i + 1]
        
        # This is a simplified measure
        if abs(swara_to_pitch(current) - swara_to_pitch(next_swara)) <= 2:
            stable_transitions += 1
    
    return stable_transitions / total_transitions if total_transitions > 0 else 1.0

def swara_to_pitch(swara):
    """Convert swara to numerical pitch value"""
    pitch_map = {
        'S': 0, 'r': 1, 'R': 2, 'g': 3, 'G': 4, 'M': 5,
        'M\'': 6, 'P': 7, 'd': 8, 'D': 9, 'n': 10, 'N': 11
    }
    return pitch_map.get(swara, 0)

def suggest_ragas_from_swaras(swara_sequence):
    """Suggest possible ragas based on detected swaras"""
    if not swara_sequence:
        return []
    
    unique_swaras = set(swara_sequence)
    
    # Define raga characteristics
    raga_swaras = {
        'yaman': {'S', 'R', 'G', 'M', 'P', 'D', 'N'},
        'bhairav': {'S', 'r', 'G', 'M', 'P', 'd', 'N'},
        'kafi': {'S', 'R', 'g', 'M', 'P', 'D', 'n'},
        'bhairavi': {'S', 'r', 'g', 'M', 'P', 'd', 'n'}
    }
    
    suggestions = []
    for raga, required_swaras in raga_swaras.items():
        if required_swaras.issubset(unique_swaras):
            match_score = len(required_swaras.intersection(unique_swaras)) / len(required_swaras)
            suggestions.append({
                "raga": raga,
                "match_score": round(match_score, 3)
            })
    
    # Sort by match score
    suggestions.sort(key=lambda x: x["match_score"], reverse=True)
    return suggestions[:3]  # Top 3 suggestions