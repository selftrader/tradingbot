import numpy as np
import pandas as pd
from dhanhq import dhanhq
from datetime import datetime, timedelta
import time
from threading import Thread

class SimpleFibonacciTrader:
    def __init__(self, client_id, access_token):
        """Initialize the trading system with DhanHQ credentials"""
        self.dhan = dhanhq(client_id=client_id, access_token=access_token)
        self.fib_levels = [0, 0.236, 0.382, 0.500, 0.618, 0.786, 1.0]
        self.active_trades = {}
        self.is_monitoring = False

    def calculate_moving_average(self, data, period=20):
        """Calculate simple moving average"""
        return data['close'].rolling(window=period).mean()

    def find_swing_points(self, data, window=10):
        """Find swing high and low points using simple method"""
        highs = []
        lows = []
        
        for i in range(window, len(data) - window):
            # Check if this is a swing high
            if all(data['high'].iloc[i] > data['high'].iloc[i-window:i]) and \
               all(data['high'].iloc[i] > data['high'].iloc[i+1:i+window+1]):
                highs.append((i, data['high'].iloc[i]))
            
            # Check if this is a swing low
            if all(data['low'].iloc[i] < data['low'].iloc[i-window:i]) and \
               all(data['low'].iloc[i] < data['low'].iloc[i+1:i+window+1]):
                lows.append((i, data['low'].iloc[i]))
        
        return highs, lows

    def calculate_fibonacci_levels(self, high_price, low_price):
        """Calculate Fibonacci retracement levels"""
        diff = high_price - low_price
        levels = {}
        
        for level in self.fib_levels:
            levels[level] = high_price - (diff * level)
            
        return levels

    def get_market_data(self, symbol, interval='1d', days=30):
        """Get market data from DhanHQ"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        try:
            data = self.dhan.historical_data(
                symbol=symbol,
                from_date=start_date.strftime('%Y-%m-%d'),
                to_date=end_date.strftime('%Y-%m-%d'),
                interval=interval
            )
            
            return pd.DataFrame(data)
        except Exception as e:
            print(f"Error fetching market data: {e}")
            return None

    def analyze_price_action(self, data, fib_levels):
        """Analyze price action relative to Fibonacci levels"""
        current_price = data['close'].iloc[-1]
        signals = []
        
        for level, price in fib_levels.items():
            # Check if price is near a Fibonacci level (within 0.5%)
            if abs(current_price - price) / price < 0.005:
                # Determine trend using simple moving averages
                ma20 = self.calculate_moving_average(data, 20).iloc[-1]
                ma50 = self.calculate_moving_average(data, 50).iloc[-1]
                
                if ma20 > ma50 and current_price > price:
                    signals.append({
                        'type': 'BUY',
                        'price': current_price,
                        'stop_loss': price * 0.99,  # 1% below support
                        'target': current_price * 1.02,  # 2% profit target
                        'fib_level': level
                    })
                elif ma20 < ma50 and current_price < price:
                    signals.append({
                        'type': 'SELL',
                        'price': current_price,
                        'stop_loss': price * 1.01,  # 1% above resistance
                        'target': current_price * 0.98,  # 2% profit target
                        'fib_level': level
                    })
        
        return signals

    def execute_trade(self, symbol, signal):
        """Execute trade based on signal"""
        try:
            trade_id = f"{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            quantity = 1  # Adjust based on your capital and risk management
            
            # Place main order
            order = self.dhan.place_order(
                security_id=symbol,
                exchange='NSE',
                transaction_type=signal['type'],
                quantity=quantity,
                order_type='LIMIT',
                product_type='INTRADAY',
                price=signal['price']
            )
            
            # Store trade information
            self.active_trades[trade_id] = {
                'symbol': symbol,
                'entry_price': signal['price'],
                'type': signal['type'],
                'quantity': quantity,
                'stop_loss': signal['stop_loss'],
                'target': signal['target'],
                'order_id': order['order_id'],
                'entry_time': datetime.now()
            }
            
            print(f"\nTrade Executed: {signal['type']} {symbol}")
            print(f"Entry Price: {signal['price']}")
            print(f"Stop Loss: {signal['stop_loss']}")
            print(f"Target: {signal['target']}")
            
            return trade_id
            
        except Exception as e:
            print(f"Error executing trade: {e}")
            return None

    def monitor_trades(self):
        """Monitor active trades and update P&L"""
        self.is_monitoring = True
        
        while self.is_monitoring and self.active_trades:
            try:
                for trade_id, trade in list(self.active_trades.items()):
                    quote = self.dhan.get_quote(trade['symbol'])
                    current_price = quote['last_traded_price']
                    
                    # Calculate P&L
                    if trade['type'] == 'BUY':
                        pnl = (current_price - trade['entry_price']) * trade['quantity']
                    else:
                        pnl = (trade['entry_price'] - current_price) * trade['quantity']
                    
                    pnl_percent = (pnl / (trade['entry_price'] * trade['quantity'])) * 100
                    
                    # Print real-time update
                    print(f"\nTrade Update ({trade['symbol']}):")
                    print(f"Current Price: {current_price}")
                    print(f"P&L: ₹{pnl:.2f} ({pnl_percent:.2f}%)")
                    
                    # Check stop loss and target
                    if trade['type'] == 'BUY':
                        if current_price <= trade['stop_loss'] or current_price >= trade['target']:
                            self.close_trade(trade_id, current_price)
                    else:  # SELL
                        if current_price >= trade['stop_loss'] or current_price <= trade['target']:
                            self.close_trade(trade_id, current_price)
                            
                time.sleep(1)  # Update every second
                
            except Exception as e:
                print(f"Error in monitoring: {e}")
                continue

    def close_trade(self, trade_id, current_price):
        """Close a trade and calculate final P&L"""
        if trade_id in self.active_trades:
            trade = self.active_trades[trade_id]
            
            try:
                # Place closing order
                close_order = self.dhan.place_order(
                    security_id=trade['symbol'],
                    exchange='NSE',
                    transaction_type='SELL' if trade['type'] == 'BUY' else 'BUY',
                    quantity=trade['quantity'],
                    order_type='MARKET',
                    product_type='INTRADAY'
                )
                
                # Calculate final P&L
                if trade['type'] == 'BUY':
                    final_pnl = (current_price - trade['entry_price']) * trade['quantity']
                else:
                    final_pnl = (trade['entry_price'] - current_price) * trade['quantity']
                
                pnl_percent = (final_pnl / (trade['entry_price'] * trade['quantity'])) * 100
                
                print(f"\nTrade Closed: {trade['symbol']}")
                print(f"Final P&L: ₹{final_pnl:.2f} ({pnl_percent:.2f}%)")
                print(f"Duration: {datetime.now() - trade['entry_time']}")
                
                del self.active_trades[trade_id]
                
            except Exception as e:
                print(f"Error closing trade: {e}")

    def run_strategy(self, symbol):
        """Main method to run the trading strategy"""
        # Get market data
        data = self.get_market_data(symbol)
        if data is None:
            return
        
        # Find swing points
        highs, lows = self.find_swing_points(data)
        if not highs or not lows:
            print("No swing points found")
            return
        
        # Get most recent swing high and low
        recent_high = max(highs, key=lambda x: x[0])[1]
        recent_low = max(lows, key=lambda x: x[0])[1]
        
        # Calculate Fibonacci levels
        fib_levels = self.calculate_fibonacci_levels(recent_high, recent_low)
        
        # Analyze price action and get signals
        signals = self.analyze_price_action(data, fib_levels)
        
        # Execute trades for valid signals
        for signal in signals:
            trade_id = self.execute_trade(symbol, signal)
            if trade_id and not self.is_monitoring:
                # Start monitoring thread if not already running
                monitor_thread = Thread(target=self.monitor_trades)
                monitor_thread.daemon = True
                monitor_thread.start()

    def stop_monitoring(self):
        """Stop the trade monitoring"""
        self.is_monitoring = False