from requests import Session
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import pandas as pd
import numpy as np
import joblib
import logging
from datetime import datetime, timedelta
from database.connection import get_db
from models.database_models import Trade, Position

logger = logging.getLogger(__name__)

class ModelTrainerService:
    def __init__(self):
        self.model_path = "models/monitoring/trading_model.joblib"
        self.metrics_path = "models/monitoring/performance_metrics.csv"
        self.model = self._load_or_create_model()
        
    def _load_or_create_model(self):
        try:
            return joblib.load(self.model_path)
        except:
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            joblib.dump(model, self.model_path)
            return model
            
    async def evaluate_model_performance(self, db: Session):
        """Evaluate model performance on recent trades"""
        recent_trades = db.query(Trade).filter(
            Trade.created_at >= datetime.now() - timedelta(days=30)
        ).all()
        
        if not recent_trades:
            return None
            
        predictions_correct = sum(1 for trade in recent_trades 
                                if trade.pnl > 0 and trade.metadata.get('confidence', 0) > 0.7)
        accuracy = predictions_correct / len(recent_trades)
        
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'accuracy': accuracy,
            'total_trades': len(recent_trades),
            'profitable_trades': sum(1 for t in recent_trades if t.pnl > 0),
            'total_pnl': sum(t.pnl for t in recent_trades),
            'average_confidence': np.mean([t.metadata.get('confidence', 0) for t in recent_trades])
        }
        
        self._save_metrics(metrics)
        return metrics