from flask import request, jsonify
from advanced_ml.advanced_models import AdvancedRagaClassifier, LSTMMusicGenerator
from utils.file_utils import FileUtils
from . import advanced_ml_bp

# Initialize advanced models
advanced_classifier = AdvancedRagaClassifier()
music_generator = LSTMMusicGenerator()

@advanced_ml_bp.route('/advanced/detect-raga', methods=['POST'])
def advanced_detect_raga():
    """Advanced raga detection"""
    try:
        if 'audio' not in request.files:
            return jsonify({"success": False, "error": "No audio file provided"}), 400
        
        audio_file = request.files['audio']
        audio_path = FileUtils.save_uploaded_file(audio_file, 'audio')
        
        result = advanced_classifier.predict_raga_advanced(audio_path)
        
        # Cleanup
        FileUtils.cleanup_file(audio_path)
        
        if "error" in result:
            return jsonify({"success": False, "error": result["error"]}), 500
        
        return jsonify({
            "success": True,
            "detection_result": result,
            "message": "Advanced AI analysis completed"
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@advanced_ml_bp.route('/advanced/generate-music', methods=['POST'])
def advanced_generate_music():
    """Advanced music generation"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No JSON data provided"}), 400
        
        raga_name = data.get('raga', 'yaman')
        length = data.get('length', 50)
        temperature = data.get('temperature', 1.0)
        
        result = music_generator.generate_composition_advanced(raga_name, length, temperature)
        
        if "error" in result:
            return jsonify({"success": False, "error": result["error"]}), 500
        
        return jsonify({
            "success": True,
            "generation_result": result,
            "message": "AI music composition generated"
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@advanced_ml_bp.route('/advanced/model-info', methods=['GET'])
def get_model_info():
    """Get information about advanced models"""
    return jsonify({
        "success": True,
        "models": {
            "raga_classifier": {
                "type": "CNN + LSTM",
                "status": "ready",
                "description": "Deep learning model for raga classification"
            },
            "music_generator": {
                "type": "LSTM Sequence Generator", 
                "status": "ready",
                "description": "AI model for music composition"
            }
        },
        "advanced_features": True
    })