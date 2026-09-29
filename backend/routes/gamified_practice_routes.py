from flask import request, jsonify, Blueprint
from advanced_ml.gamified_practice import GamifiedPracticeEngine
from utils.file_utils import FileUtils

gamified_practice_bp = Blueprint('gamified_practice', __name__)
practice_engine = GamifiedPracticeEngine()

@gamified_practice_bp.route('/practice/assess-performance', methods=['POST'])
def assess_performance():
    """Assess student performance from audio"""
    try:
        if 'audio' not in request.files:
            return jsonify({"success": False, "error": "No audio file provided"}), 400
        
        audio_file = request.files['audio']
        data = request.form
        
        # Save audio file
        audio_path = FileUtils.save_uploaded_file(audio_file, 'audio')
        
        # Get exercise details
        target_exercise = {
            'name': data.get('exercise_name', 'Basic Swara Practice'),
            'raga': data.get('raga', 'yaman'),
            'level': data.get('level', 'beginner')
        }
        
        # Assess performance
        result = practice_engine.assess_performance(audio_path, target_exercise)
        
        # Cleanup
        FileUtils.cleanup_file(audio_path)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@gamified_practice_bp.route('/practice/generate-exercise', methods=['POST'])
def generate_exercise():
    """Generate personalized practice exercise"""
    try:
        data = request.get_json()
        
        student_level = data.get('level', 'beginner')
        target_raga = data.get('raga', 'yaman')
        focus_areas = data.get('focus_areas', [])
        
        result = practice_engine.generate_personalized_exercise(
            student_level, target_raga, focus_areas
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@gamified_practice_bp.route('/practice/student-progress', methods=['GET'])
def get_student_progress():
    """Get student progress report"""
    try:
        student_id = request.args.get('student_id', 'current_student')
        result = practice_engine.get_student_progress(student_id)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@gamified_practice_bp.route('/practice/daily-challenge', methods=['GET'])
def get_daily_challenge():
    """Get daily practice challenge"""
    try:
        student_id = request.args.get('student_id', 'current_student')
        progress = practice_engine.get_student_progress(student_id)
        
        current_level = "beginner"
        if progress.get('success'):
            current_level = progress['progress_report']['current_level']
        
        # Generate daily challenge
        challenges = {
            'beginner': {
                "title": "Swara Foundation",
                "description": "Perfect your basic swaras with focused practice",
                "exercise": "S R G M P D N S' - S' N D P M G R S",
                "duration": "10 minutes",
                "reward": "5 stars",
                "focus": "Pitch accuracy and smooth transitions"
            },
            'intermediate': {
                "title": "Raga Exploration", 
                "description": "Deepen your understanding of raga characteristics",
                "exercise": "Practice characteristic phrases of your chosen raga",
                "duration": "15 minutes", 
                "reward": "8 stars",
                "focus": "Raga bhava and phrase development"
            },
            'advanced': {
                "title": "Creative Improvisation",
                "description": "Develop your improvisational skills",
                "exercise": "Create variations on a basic theme",
                "duration": "20 minutes",
                "reward": "12 stars", 
                "focus": "Spontaneity and musical creativity"
            }
        }
        
        challenge = challenges.get(current_level, challenges['beginner'])
        
        return jsonify({
            "success": True,
            "daily_challenge": challenge,
            "level": current_level
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@gamified_practice_bp.route('/practice/achievements', methods=['GET'])
def get_achievements():
    """Get student achievements and badges"""
    try:
        student_id = request.args.get('student_id', 'current_student')
        progress = practice_engine.get_student_progress(student_id)
        
        if not progress.get('success'):
            return jsonify({"success": False, "error": "No progress data"})
        
        progress_data = progress['progress_report']
        
        # Calculate achievements
        achievements = []
        
        if progress_data['total_sessions'] >= 1:
            achievements.append({
                "name": "First Steps",
                "description": "Complete your first practice session",
                "icon": "🎵",
                "unlocked": True
            })
        
        if progress_data['total_sessions'] >= 10:
            achievements.append({
                "name": "Dedicated Student", 
                "description": "Complete 10 practice sessions",
                "icon": "⭐",
                "unlocked": True
            })
        
        if progress_data['average_accuracy'] >= 80:
            achievements.append({
                "name": "Precision Master",
                "description": "Maintain 80% average accuracy",
                "icon": "🎯", 
                "unlocked": True
            })
        
        if progress_data['total_stars'] >= 50:
            achievements.append({
                "name": "Star Collector",
                "description": "Earn 50 stars total",
                "icon": "✨",
                "unlocked": True
            })
        
        # Add locked achievements
        if progress_data['total_sessions'] < 10:
            achievements.append({
                "name": "Marathon Runner",
                "description": "Complete 50 practice sessions", 
                "icon": "🏃",
                "unlocked": False
            })
        
        return jsonify({
            "success": True,
            "achievements": achievements,
            "total_achievements": len([a for a in achievements if a['unlocked']])
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500