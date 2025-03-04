from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import Position, Trade
from services.strategy_service import StrategyService
from services.model_trainer_service import ModelTrainerService
from typing import List, Dict
import asyncio
import logging
from datetime import datetime
import pandas as pd
import numpy as np
from services.live_market_service import LiveMarketService
from services.upstox_service import UpstoxService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/monitor", tags=["monitoring"])

class AutoTrader:
    def __init__(self, db: Session):
        self.strategy_service = StrategyService(db)
        # self.trading_service = TradingService(db)
        self.model_trainer = ModelTrainerService()
        self.is_active = False
        self.min_confidence = 0.7
        self.max_positions = 5
        self.position_size = 100000  # ₹1 Lakh per trade
        self.last_evaluation_time = datetime.now()
        self.evaluation_interval = 3600  # 1 hour
        self.stop_loss_pct = 0.02  # 2% stop loss
        self.target_pct = 0.03     # 3% target
        self.trailing_stop_pct = 0.01  # 1% trailing stop

        # Initialize broker service
        self.broker = UpstoxService(
            api_key="YOUR_API_KEY",
            api_secret="YOUR_API_SECRET",
            redirect_uri="YOUR_REDIRECT_URI"
        )
        self.live_market = LiveMarketService(self.broker)
        # self.predictor = AdvancedStockPredictor()

    async def start(self):
        """Start trading with broker connection"""
        await self.broker.connect()
        self.is_active = True

    async def analyze_and_trade(self, symbol: str, db: Session):
        """Real-time analysis and trading"""
        try:
            # Get live market data
            live_data = await self.live_market.get_live_data(symbol)
            current_price = live_data['price']
            
            # Get AI analysis
            analysis = await self.strategy_service.analyze_stock(symbol)
            
            # Check existing position
            position = db.query(Position).filter(
                Position.symbol == symbol,
                Position.is_active == True
            ).first()
            
            if position:
                await self._manage_position(position, current_price, analysis, db)
            elif analysis['confidence'] >= self.min_confidence:
                await self._open_position(symbol, current_price, analysis, db)
                
        except Exception as e:
            logger.error(f"Trading error for {symbol}: {e}")
    
    async def _manage_position(self, position: Position, current_price: float, 
                             analysis: Dict, db: Session):
        """Manage existing position"""
        try:
            # Calculate P&L
            pnl_pct = (current_price - position.entry_price) / position.entry_price
            
            # Update trailing stop loss
            new_stop_loss = current_price * (1 - self.trailing_stop_pct)
            if new_stop_loss > position.stop_loss:
                position.stop_loss = new_stop_loss
                db.commit()
            
            # Check exit conditions
            should_exit = (
                current_price <= position.stop_loss or  # Stop loss hit
                current_price >= position.target or     # Target hit
                (analysis['signal'] == "SELL" and      # AI suggests exit
                 analysis['confidence'] >= 0.8)
            )
            
            if should_exit:
                await self.trading_service.close_position(
                    position_id=position.id,
                    exit_price=current_price,
                    exit_reason="Stop Loss" if current_price <= position.stop_loss else
                              "Target Hit" if current_price >= position.target else
                              "AI Signal",
                    db=db
                )
                logger.info(f"Position closed: {position.symbol} PnL: {pnl_pct:.2%}")
                
        except Exception as e:
            logger.error(f"Position management error: {e}")
    
    async def _open_position(self, symbol: str, current_price: float, 
                           analysis: Dict, db: Session):
        """Open new position"""
        try:
            quantity = self._calculate_position_size(current_price)
            
            # Set stop loss and target
            stop_loss = current_price * (1 - self.stop_loss_pct)
            target = current_price * (1 + self.target_pct)
            
            await self.trading_service.execute_trade(
                symbol=symbol,
                action=analysis['signal'],
                quantity=quantity,
                price=current_price,
                stop_loss=stop_loss,
                target=target,
                metadata={
                    'confidence': analysis['confidence'],
                    'analysis_metrics': analysis['metrics']
                },
                db=db
            )
            
            logger.info(f"New position opened: {symbol} {analysis['signal']}")
            
        except Exception as e:
            logger.error(f"Position opening error: {e}")

    def _calculate_position_size(self, current_price: float) -> int:
        """Calculate quantity based on position size"""
        return int(self.position_size / current_price)

# Update the auto_trader initialization
def get_auto_trader(db: Session = Depends(get_db)):
    return AutoTrader(db)

# Modify the router endpoints to use the get_auto_trader dependency
@router.post("/auto-trading/start")
async def start_auto_trading(
    symbols: List[str], 
    auto_trader: AutoTrader = Depends(get_auto_trader),
    db: Session = Depends(get_db)
):
    """Start autonomous trading"""
    try:
        auto_trader.is_active = True
        
        # Start continuous monitoring and trading
        async def trading_loop():
            while auto_trader.is_active:
                for symbol in symbols:
                    await auto_trader.analyze_and_trade(symbol, db)
                await asyncio.sleep(300)  # 5-minute interval
        
        asyncio.create_task(trading_loop())
        return {"message": "Autonomous trading started", "symbols": symbols}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/auto-trading/stop")
async def stop_auto_trading(auto_trader: AutoTrader = Depends(get_auto_trader)):
    """Stop autonomous trading"""
    auto_trader.is_active = False
    return {"message": "Autonomous trading stopped"}

@router.get("/positions")
async def get_positions(db: Session = Depends(get_db)):
    """Get current open positions"""
    positions = db.query(Position).filter(Position.is_active == True).all()
    return positions

@router.get("/positions/{symbol}")
async def get_position_details(
    symbol: str, 
    auto_trader: AutoTrader = Depends(get_auto_trader),
    db: Session = Depends(get_db)
):
    """Get detailed position information"""
    try:
        position = db.query(Position).filter(
            Position.symbol == symbol,
            Position.is_active == True
        ).first()
        
        if not position:
            return {"message": f"No active position for {symbol}"}
        
        live_data = await auto_trader.live_market.get_live_data(symbol)
        current_price = live_data['price']
        
        return {
            "symbol": position.symbol,
            "entry_price": position.entry_price,
            "current_price": current_price,
            "quantity": position.quantity,
            "pnl": (current_price - position.entry_price) * position.quantity,
            "pnl_percentage": ((current_price - position.entry_price) / 
                             position.entry_price) * 100,
            "stop_loss": position.stop_loss,
            "target": position.target,
            "position_age": (datetime.now() - position.created_at).seconds / 3600,
            "market_data": live_data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/performance")
async def get_performance(db: Session = Depends(get_db)):
    """Get trading performance metrics"""
    trades = db.query(Trade).all()
    active_positions = db.query(Position).filter(Position.is_active == True).all()
    
    return {
        "total_trades": len(trades),
        "successful_trades": len([t for t in trades if t.pnl > 0]),
        "total_pnl": sum(t.pnl for t in trades),
        "win_rate": len([t for t in trades if t.pnl > 0]) / len(trades) if trades else 0,
        "active_positions": len(active_positions),
        "current_exposure": sum(p.quantity * p.average_price for p in active_positions),
        "unrealized_pnl": sum(p.unrealized_pnl for p in active_positions)
    }

@router.get("/model/performance")
async def get_model_performance(db: Session = Depends(get_db)):
    """Get model performance metrics"""
    try:
        metrics_df = pd.read_csv("models/monitoring/performance_metrics.csv")
        latest_metrics = metrics_df.iloc[-1].to_dict()
        
        # Calculate trends
        recent_metrics = metrics_df.tail(10)
        trends = {
            'accuracy_trend': recent_metrics['accuracy'].mean(),
            'pnl_trend': recent_metrics['total_pnl'].mean(),
            'confidence_trend': recent_metrics['average_confidence'].mean()
        }
        
        return {
            "current_metrics": latest_metrics,
            "trends": trends,
            "total_trades_analyzed": metrics_df['total_trades'].sum(),
            "last_evaluation": latest_metrics['timestamp']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/model/daily-report")
async def get_daily_report(db: Session = Depends(get_db)):
    """Get daily model performance report"""
    try:
        today = datetime.now().date()
        today_trades = db.query(Trade).filter(
            Trade.created_at >= today
        ).all()
        
        return {
            "date": today.isoformat(),
            "total_trades": len(today_trades),
            "successful_predictions": sum(1 for t in today_trades if t.pnl > 0),
            "total_pnl": sum(t.pnl for t in today_trades),
            "average_confidence": np.mean([t.metadata.get('confidence', 0) 
                                         for t in today_trades])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/predict/advanced")
async def get_advanced_predictions(
    auto_trader: AutoTrader = Depends(get_auto_trader),
    db: Session = Depends(get_db)
):
    """Get comprehensive trading predictions"""
    try:
        predictions = await auto_trader.predictor.predict_trades(db)
        
        # Store predictions in database
        prediction_record = Trade(
            trade_type="AI_PREDICTION",
            metadata=predictions,
            created_at=datetime.now()
        )
        db.add(prediction_record)
        db.commit()
        
        return {
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "predictions": predictions,
            "analysis_id": prediction_record.id
        }
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))