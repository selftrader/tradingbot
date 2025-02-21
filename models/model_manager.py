import os
import joblib
from models.train_ai_model import train_model  # Import Training Script

class ModelManager:
    def __init__(self):
        """Manages AI Models for Index, Options, and Stocks"""
        self.models = {
            "index": self.load_model("models/index_model.pkl"),
            "options": self.load_model("models/options_model.pkl"),
            "stocks": self.load_model("models/stocks_model.pkl")
        }

    def load_model(self, model_path):
        """Loads AI Model, Trains If Not Found"""
        if not os.path.exists(model_path):
            print(f"⚠️ Model not found: {model_path}. Training now...")
            train_model()  # ✅ Automatically Train Model
            if not os.path.exists(model_path):
                raise Exception(f"❌ Model Training Failed: {model_path} not found.")
        return joblib.load(model_path)  # ✅ Load Trained Model

    def predict(self, model_type, data):
        """Predicts using the AI Model"""
        if model_type in self.models:
            return self.models[model_type].predict([data])[0]
        else:
            raise ValueError(f"Invalid model type: {model_type}")
