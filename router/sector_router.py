import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict

from services.sector_analyzer import SectorAnalyzer
from database.connection import get_db  # Updated import path
from config import SECTORAL_INDICES

router = APIRouter()

@router.get("/api/sectors")
async def get_sectors():
    """Get list of available sectors"""
    return list(SECTORAL_INDICES.keys())

@router.get("/api/sectors/{sector_name}/analysis")
async def analyze_sector(
    sector_name: str,
    db: Session = Depends(get_db)
):
    """Analyze stocks in a specific sector"""
    try:
        if sector_name not in SECTORAL_INDICES:
            raise HTTPException(status_code=404, detail="Sector not found")
        
        analyzer = SectorAnalyzer(db)
        results = await analyzer.analyze_sector(sector_name)
        
        # Filter for strong signals (probability > 0.7)
        recommendations = [
            {
                "symbol": r["symbol"],
                "action": "BUY" if r["prediction"] > 0 else "SELL",
                "confidence": f"{r['probability']*100:.1f}%",
                "indicators": r["indicators"]
            }
            for r in results
            if r["probability"] > 0.7
        ]
        
        return {
            "sector": sector_name,
            "timestamp": datetime.now().isoformat(),
            "recommendations": recommendations
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))