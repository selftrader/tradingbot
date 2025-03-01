import asyncio
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import yfinance as yf
import logging
import torch
import torch.nn.functional as F
from torch.utils.data import DataLoader
from datetime import datetime
import json
from typing import List
import os
from services.broker_service import UpstoxBroker
from dotenv import load_dotenv

from models.training_report import TrainingReport

logger = logging.getLogger(__name__)

class ModelTrainer:
    def __init__(self):
        self.model_path = "models/saved/trading_model.joblib"
        self.training_symbols = [
            "RELIANCE.NS", 
            "TCS.NS", 
            "INFY.NS",
            "HDFCBANK.NS"
        ]
        self.features = [
            'SMA20', 'SMA50', 'RSI', 
            'Returns', 'Volatility', 'Volume_Ratio'
        ]
        self.broker_api = self._initialize_broker()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
    def _initialize_broker(self) -> UpstoxBroker:
        """Initialize broker API connection"""
        try:
            load_dotenv()  # Load environment variables
            api_key = os.getenv('UPSTOX_API_KEY')
            api_secret = os.getenv('UPSTOX_API_SECRET')
            
            if not api_key or not api_secret:
                raise ValueError("Broker API credentials not found in environment variables")
                
            return UpstoxBroker(api_key, api_secret)
            
        except Exception as e:
            logger.error(f"Failed to initialize broker: {e}")
            raise

    def train(self):
        """Main training pipeline"""
        try:
            # 1. Data Collection
            training_data = self._collect_training_data()
            
            # 2. Feature Engineering
            X, y = self._prepare_features(training_data)
            
            # 3. Model Training
            model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            model.fit(X, y)
            
            # 4. Save Model
            joblib.dump(model, self.model_path)
            logger.info(f"Model saved to {self.model_path}")
            
            return model
            
        except Exception as e:
            logger.error(f"Training failed: {str(e)}")
            raise

    def _collect_training_data(self):
        """Collect historical data for training"""
        all_data = []
        for symbol in self.training_symbols:
            data = yf.download(
                symbol, 
                period="2y",    # 2 years of historical data
                interval="1d"   # Daily timeframe
            )
            all_data.append(data)
        return pd.concat(all_data)

    def _prepare_features(self, data: pd.DataFrame):
        """Prepare features for training"""
        df = data.copy()
        
        # Technical indicators
        df['SMA20'] = df['Close'].rolling(window=20).mean()
        df['SMA50'] = df['Close'].rolling(window=50).mean()
        df['RSI'] = self._calculate_rsi(df['Close'])
        df['Returns'] = df['Close'].pct_change()
        df['Volatility'] = df['Returns'].rolling(window=20).std()
        df['Volume_Ratio'] = df['Volume'] / df['Volume'].rolling(window=20).mean()
        
        # Target: Price direction (1 for up, 0 for down)
        df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
        
        # Drop NaN values
        df = df.dropna()
        
        return df[self.features], df['Target']

    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

def calculate_loss(action_probs, value, rewards, actions_taken, beta=0.01):
    """
    Calculate the total loss combining actor and critic losses
    
    Args:
        action_probs: Predicted action probabilities from actor
        value: Predicted state value from critic
        rewards: Actual rewards received
        actions_taken: Actions that were actually taken
        beta: Entropy coefficient for exploration
    """
    # Convert to tensors if not already
    rewards = torch.FloatTensor(rewards)
    actions_taken = torch.LongTensor(actions_taken)
    
    # Actor loss (policy gradient)
    selected_action_probs = action_probs.gather(1, actions_taken.unsqueeze(1))
    actor_loss = -torch.log(selected_action_probs) * rewards
    
    # Critic loss (value prediction)
    critic_loss = F.mse_loss(value.squeeze(), rewards)
    
    # Entropy loss (for exploration)
    entropy = -(action_probs * torch.log(action_probs)).sum(dim=1).mean()
    
    # Total loss
    total_loss = actor_loss.mean() + critic_loss - beta * entropy
    
    return total_loss

async def train_ai_model(symbols: List[str], epochs: int = 100):
    """Train the AI model with the given symbols"""
    trainer = ModelTrainer()
    
    try:
        logger.info(f"Starting AI model training with {len(symbols)} symbols")
        
        # Training loop implementation
        for epoch in range(epochs):
            for symbol in symbols:
                # Get training data
                market_data = await trainer.broker_api.get_historical_data(symbol)
                features, targets = trainer._prepare_features(market_data)
                
                # Training logic here
                # ... implementation of training steps ...
                
            logger.info(f"Completed epoch {epoch + 1}/{epochs}")
            
        logger.info("Training completed successfully")
        
    except Exception as e:
        logger.error(f"Training error: {e}")
        raise
    finally:
        # Cleanup
        if hasattr(trainer, 'broker_api'):
            await trainer.broker_api.close()

def save_checkpoint(model, optimizer, epoch, loss):
    """Save training checkpoint"""
    checkpoint = {
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'loss': loss
    }
    path = f'models/saved/checkpoints/ai_trader_checkpoint_{epoch}.pth'
    torch.save(checkpoint, path)

def save_final_model(model, history):
    """Save final model and training history"""
    # Save model
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    model_path = f'models/saved/ai_trader_{timestamp}.pth'
    torch.save(model.state_dict(), model_path)
    
    # Save training history
    history_path = f'models/saved/training_history_{timestamp}.json'
    with open(history_path, 'w') as f:
        json.dump(history, f)
    
    return model_path

async def simulate_trades(symbol: str, actions: torch.Tensor, market_data: torch.Tensor) -> List[float]:
    """Simulate trades to calculate rewards"""
    rewards = []
    
    for i, action in enumerate(actions):
        if i >= len(market_data) - 1:
            rewards.append(0)  # No reward for last data point
            continue
            
        current_price = market_data[i][-1]  # Assuming last feature is price
        next_price = market_data[i + 1][-1]
        
        if action == 0:  # BUY
            reward = (next_price - current_price) / current_price
        elif action == 1:  # SELL
            reward = (current_price - next_price) / current_price
        else:  # HOLD
            reward = 0
            
        rewards.append(float(reward))
    
    return rewards

# Train all models
trainer = ModelTrainer()
trainer.train()

# Train all models & generate reports
TrainingReport("index_model", "nifty50_data").train_model()
TrainingReport("options_model", "nifty_options_data").train_model()
TrainingReport("stock_model", "reliance_data").train_model()
TrainingReport("sectoral_model", "nifty_it_data").train_model()

# Usage example
if __name__ == "__main__":
    symbols = [
        "RELIANCE.NS", 
        "TCS.NS", 
        "INFY.NS",
        "HDFCBANK.NS",
        "NIFTY50.NS"
    ]
    
    asyncio.run(train_ai_model(symbols, epochs=100))