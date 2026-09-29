from flask import Blueprint

# Create blueprints
emotion_bp = Blueprint('emotion', __name__, url_prefix='/api')
midi_bp = Blueprint('midi', __name__, url_prefix='/api')
raga_bp = Blueprint('raga', __name__, url_prefix='/api')
swara_bp = Blueprint('swara', __name__, url_prefix='/api')
advanced_ml_bp = Blueprint('advanced_ml', __name__, url_prefix='/api')