import torch
import torch.nn as nn
import numpy as np
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class LSTMPricePredictor(nn.Module):
    def __init__(self, input_size: int = 10, hidden_size: int = 64, num_layers: int = 2):
        super(LSTMPricePredictor, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        
        # LSTM layers
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=0.2
        )
        
        # Attention mechanism
        self.attention = nn.Sequential(
            nn.Linear(hidden_size, hidden_size),
            nn.Tanh(),
            nn.Linear(hidden_size, 1)
        )
        
        # Output layers
        self.fc = nn.Sequential(
            nn.Linear(hidden_size, 32),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 2)  # [price_direction, confidence]
        )

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        # LSTM forward pass
        lstm_out, _ = self.lstm(x)
        
        # Apply attention
        attention_weights = torch.softmax(self.attention(lstm_out), dim=1)
        context_vector = torch.sum(attention_weights * lstm_out, dim=1)
        
        # Generate prediction
        output = self.fc(context_vector)
        
        direction = torch.sign(output[:, 0])
        confidence = torch.sigmoid(output[:, 1])
        
        return direction, confidence