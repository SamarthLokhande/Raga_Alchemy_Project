from .emotion_model import EmotionModel
from .raga_model import RagaModel
from .swara_model import SwaraModel

class ModelManager:
    def __init__(self):
        self.emotion_model = None
        self.raga_model = None
        self.swara_model = None
        self.models_loaded = False
    
    def load_advanced_models(self):
        """Load all ML models"""
        try:
            print("📊 Loading Emotion Model...")
            self.emotion_model = EmotionModel()
            self.emotion_model.load()
            
            print("🎵 Loading Raga Model...")
            self.raga_model = RagaModel()
            self.raga_model.load()
            
            print("🎼 Loading Swara Model...")
            self.swara_model = SwaraModel()
            self.swara_model.load()
            
            self.models_loaded = True
            print("✅ All models loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            self.models_loaded = False
    
    def get_emotion_model(self):
        return self.emotion_model
    
    def get_raga_model(self):
        return self.raga_model
    
    def get_swara_model(self):
        return self.swara_model

# Global model manager instance
model_manager = ModelManager()