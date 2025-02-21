import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List
from models.ml_model import SectoralMLModel
from models.sector_analysis import SectorAnalysis
from config import SECTORAL_INDICES, PREDICTOR_CONFIG

class SectorAnalyzer:
    def __init__(self, db_session):
        self.db = db_session
        self.model = SectoralMLModel()
    
    async def analyze_sector(self, sector_name: str) -> List[Dict]:
        stocks = SECTORAL_INDICES.get(sector_name, [])
        analysis_results = []
        
        for symbol in stocks:
            try:
                # Get historical data
                end_date = datetime.now()
                start_date = end_date - timedelta(days=60)  # More data for better analysis
                df = yf.download(symbol, start=start_date, end=end_date, interval='1d')
                
                if df.empty:
                    continue
                
                # Analyze stock using ML model
                analysis = self.model.analyze_stock(df)
                if analysis:
                    analysis['symbol'] = symbol
                    
                    # Save to database
                    db_analysis = SectorAnalysis(
                        sector=sector_name,
                        symbol=symbol,
                        prediction=analysis['prediction'],
                        probability=analysis['probability'],
                        technical_indicators=analysis['indicators']
                    )
                    self.db.add(db_analysis)
                    analysis_results.append(analysis)
                    
            except Exception as e:
                print(f"Error analyzing {symbol}: {str(e)}")
                continue
        
        self.db.commit()
        return analysis_results