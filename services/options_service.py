import datetime
from typing import List, Dict
from models.options_analyzer import OptionsChainAnalyzer
from config import SECTORAL_INDICES

class OptionsService:
    def __init__(self):
        self.analyzer = OptionsChainAnalyzer()

    async def analyze_sector_options(self, sector_name: str) -> Dict:
        """Analyze options for all stocks in a sector"""
        stocks = SECTORAL_INDICES.get(sector_name, [])
        analysis_results = []

        for symbol in stocks:
            result = self.analyzer.analyze_options(symbol)
            if result and result['opportunities']:
                analysis_results.append(result)

        return {
            'sector': sector_name,
            'timestamp': datetime.now().isoformat(),
            'recommendations': self._rank_opportunities(analysis_results)
        }

    def _rank_opportunities(self, results: List[Dict]) -> List[Dict]:
        """Rank trading opportunities based on probability and risk/reward"""
        all_opportunities = []
        
        for result in results:
            for opp in result['opportunities']:
                opportunity = {
                    'symbol': result['symbol'],
                    'current_price': result['current_price'],
                    **opp,
                    'score': opp['probability'] * opp['risk_reward']
                }
                all_opportunities.append(opportunity)

        # Sort by score descending
        return sorted(all_opportunities, key=lambda x: x['score'], reverse=True)