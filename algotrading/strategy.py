# strategy.py
import pandas as pd
import numpy as np

def calculate_ema(data, period):
    """Calculate Exponential Moving Average (EMA)"""
    return data['Close'].ewm(span=period, adjust=False).mean()

def calculate_rsi(data, period=14):
    """Calculate Relative Strength Index (RSI)"""
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_fibonacci_retracement(data):
    """Calculate Fibonacci retracement levels"""
    max_price = data['Close'].max()
    min_price = data['Close'].min()
    diff = max_price - min_price
    
    levels = {
        '23.6': max_price - 0.236 * diff,
        '38.2': max_price - 0.382 * diff,
        '50.0': max_price - 0.5 * diff,
        '61.8': max_price - 0.618 * diff
    }
    return levels

def apply_trading_strategy(data):
    """Apply EMA, RSI, and Fibonacci Strategy"""
    
    # Calculate indicators
    short_ema = calculate_ema(data, 12)
    long_ema = calculate_ema(data, 26)
    rsi = calculate_rsi(data)
    fib_levels = calculate_fibonacci_retracement(data)
    
    # Strategy Logic
    action = ""
    
    # Check EMA crossover for buy/sell signals
    if short_ema[-1] > long_ema[-1]:  # Buy Signal
        action = "BUY"
    elif short_ema[-1] < long_ema[-1]:  # Sell Signal
        action = "SELL"
    
    # Check RSI for overbought/oversold conditions
    if rsi[-1] < 30:  # Oversold, Buy Signal
        action = "BUY"
    elif rsi[-1] > 70:  # Overbought, Sell Signal
        action = "SELL"
    
    # Use Fibonacci levels for buy/sell confirmation
    if data['Close'][-1] < fib_levels['38.2']:  # Close price below 38.2%, potential buy
        action = "BUY"
    elif data['Close'][-1] > fib_levels['61.8']:  # Close price above 61.8%, potential sell
        action = "SELL"
    
    return action
