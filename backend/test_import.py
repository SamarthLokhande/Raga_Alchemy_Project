# test_import.py
try:
    from advanced_ml.emotion_model import EmotionModel
    print("✅ SUCCESS: EmotionModel imported from advanced_ml")
    
    emotion_model = EmotionModel()
    emotion_model.load()
    print("✅ SUCCESS: EmotionModel instantiated and loaded")
    
except ImportError as e:
    print(f"❌ IMPORT ERROR: {e}")
except Exception as e:
    print(f"❌ OTHER ERROR: {e}")