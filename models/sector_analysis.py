from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class SectorAnalysis(Base):
    __tablename__ = "sector_analysis"

    id = Column(Integer, primary_key=True, index=True)
    sector = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    prediction = Column(Float)
    probability = Column(Float)
    technical_indicators = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)