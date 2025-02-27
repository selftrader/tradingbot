from typing import List, Dict
import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

class StockAnalyzer:
    def __init__(self):
        self.market_data_cache = {}
        
    async def analyze_sector_stocks(self, sector: str, symbols: List[str]) -> List[Dict]:
        """Analyze all stocks in a sector and return top trading opportunities"""
        signals = []
        market_data = await self._get_market_data()
        
        for symbol in symbols:
            try:
                # Get historical data
                data = await self._get_stock_data(symbol)
                if data is None:
                    continue
                
                # Analyze stock
                signal = self.selector.analyze_stock(symbol, sector, data, market_data)
                if signal:
                    signals.append(signal)
                    
            except Exception as e:
                print(f"Error analyzing {symbol}: {str(e)}")
                continue
        
        # Sort signals by strength and risk-reward
        return sorted(
            signals,
            key=lambda x: (x.signal_strength, x.risk_reward),
            reverse=True
        )

    async def _get_market_data(self) -> Dict:
        """Get overall market data and indicators"""
        try:
            nifty_data = yf.download('^NSEI', period='1y', interval='1d')
            advance_decline = await self._get_advance_decline()
            fii_dii_data = await self._get_fii_dii_data()
            
            return {
                'nifty_data': nifty_data,
                'market_breadth': advance_decline['ratio'],
                'sector_momentum': self._calculate_sector_momentum(),
                'pcr': await self._get_nifty_pcr(),
                'oi_change': await self._get_oi_change(),
                'fii_dii_net': fii_dii_data['net_activity']
            }
        except Exception as e:
            print(f"Error getting market data: {str(e)}")
            return {}

    async def _get_stock_data(self, symbol: str) -> pd.DataFrame:
        """Get historical stock data with delivery percentage"""
        try:
            data = yf.download(symbol, period='1y', interval='1d')
            # Add delivery percentage data here if available
            data['Delivery_Percentage'] = 0  # Replace with actual delivery data
            return data
        except Exception:
            return None