from flask import request, jsonify
import os
from datetime import datetime
from utils.file_utils import FileUtils
from models.model_manager import model_manager
from advanced_ml.advanced_models import AdvancedRagaClassifier
from . import raga_bp

@raga_bp.route('/detect-raga', methods=['POST'])
def detect_raga():
    """Detect raga from audio input"""
    try:
        print("🎵 Received raga detection request")
        
        if 'audio' not in request.files:
            return jsonify({
                "success": False,
                "error": "No audio file provided"
            }), 400

        audio_file = request.files['audio']
        
        # Validate file
        if audio_file.filename == '':
            return jsonify({
                "success": False,
                "error": "No file selected"
            }), 400

        # Save uploaded file
        try:
            audio_path = FileUtils.save_uploaded_file(audio_file, 'audio')
            print(f"✅ Audio saved to: {audio_path}")
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 400

        # Use advanced classifier for better accuracy
        advanced_classifier = AdvancedRagaClassifier()
        result = advanced_classifier.predict_raga_advanced(audio_path)
        
        # Clean up uploaded file
        FileUtils.cleanup_file(audio_path)

        if "error" in result:
            return jsonify({
                "success": False,
                "error": result["error"]
            }), 500

        response = {
            "success": True,
            "detection_result": result,
            "message": "Raga analysis completed successfully"
        }
        
        print(f"🎶 Raga detected: {result.get('raga', 'unknown')}")
        return jsonify(response)

    except Exception as e:
        print(f"❌ Raga detection failed: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Raga detection failed: {str(e)}"
        }), 500

@raga_bp.route('/supported-ragas', methods=['GET'])
def get_supported_ragas():
    """Get list of all supported ragas"""
    return jsonify({
        "success": True,
        "ragas": [
            {"name": "Yaman", "value": "yaman", "time": "Evening", "mood": "Peaceful"},
            {"name": "Bhairav", "value": "bhairav", "time": "Morning", "mood": "Devotional"},
            {"name": "Malkauns", "value": "malkauns", "time": "Night", "mood": "Serious"},
            {"name": "Kafi", "value": "kafi", "time": "Night", "mood": "Romantic"},
            {"name": "Bhairavi", "value": "bhairavi", "time": "Morning", "mood": "Devotional"},
            {"name": "Todi", "value": "todi", "time": "Morning", "mood": "Serious"},
            {"name": "Asavari", "value": "asavari", "time": "Morning", "mood": "Sad"},
            {"name": "Khamaj", "value": "khamaj", "time": "Evening", "mood": "Romantic"},
            {"name": "Kalyan", "value": "kalyan", "time": "Evening", "mood": "Happy"},
            {"name": "Kedar", "value": "kedar", "time": "Night", "mood": "Romantic"}
        ]
    })