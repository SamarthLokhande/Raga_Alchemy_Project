from flask import request, jsonify
import os
from datetime import datetime
from utils.file_utils import FileUtils
from models.model_manager import model_manager
from . import emotion_bp

@emotion_bp.route('/emotion-to-raga', methods=['POST'])
def emotion_to_raga():
    """Detect emotion from image and recommend ragas"""
    try:
        print("📸 Received emotion detection request")
        
        if 'image' not in request.files:
            return jsonify({
                "success": False,
                "error": "No image file provided"
            }), 400

        image_file = request.files['image']
        
        # Validate file
        if image_file.filename == '':
            return jsonify({
                "success": False,
                "error": "No file selected"
            }), 400

        # Save uploaded file
        try:
            image_path = FileUtils.save_uploaded_file(image_file, 'image')
            print(f"✅ Image saved to: {image_path}")
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 400

        # Get emotion model and detect emotion
        emotion_model = model_manager.get_emotion_model()
        emotion_result = emotion_model.detect_emotion(image_path)

        # Clean up uploaded file
        FileUtils.cleanup_file(image_path)

        if emotion_result.get('error'):
            return jsonify({
                "success": False,
                "error": emotion_result['error']
            }), 500

        # Map emotion to ragas
        emotion = emotion_result['emotion']
        recommended_ragas = get_ragas_for_emotion(emotion)
        
        response = {
            "success": True,
            "emotion_analysis": emotion_result,
            "recommended_ragas": recommended_ragas,
            "suggestions": get_emotion_suggestions(emotion)
        }
        
        print(f"🎭 Emotion detected: {emotion}, Recommended ragas: {recommended_ragas}")
        return jsonify(response)

    except Exception as e:
        print(f"❌ Emotion detection failed: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Emotion detection failed: {str(e)}"
        }), 500

def get_ragas_for_emotion(emotion):
    """Map emotion to appropriate ragas"""
    emotion_raga_mapping = {
        'happy': ['yaman', 'khamaj', 'kalyan', 'kedar'],
        'sad': ['asavari', 'bhairavi', 'malkauns'],
        'angry': ['bhairav', 'todi', 'lalit'],
        'surprise': ['malkauns', 'kedar', 'shree'],
        'fear': ['asavari', 'todi', 'marwa'],
        'disgust': ['bhairav', 'malkauns'],
        'neutral': ['yaman', 'kafi', 'bageshree'],
        'peaceful': ['yaman', 'bhairavi', 'ahir_bhairav'],
        'romantic': ['kafi', 'khamaj', 'kedar', 'pilu'],
        'devotional': ['bhairav', 'bhairavi', 'ahir_bhairav']
    }
    
    return emotion_raga_mapping.get(emotion, ['yaman', 'bhairavi'])

def get_emotion_suggestions(emotion):
    """Get suggestions based on detected emotion"""
    suggestions = {
        'happy': "Perfect time for joyful and uplifting ragas!",
        'sad': "Let the healing power of music uplift your spirits.",
        'angry': "Calming ragas to soothe your mind and bring peace.",
        'peaceful': "Enjoy the serenity with meditative ragas.",
        'romantic': "Experience the beauty of love through music.",
        'devotional': "Connect with the divine through spiritual ragas."
    }
    
    return suggestions.get(emotion, "Enjoy the perfect raga for your current state of mind.")