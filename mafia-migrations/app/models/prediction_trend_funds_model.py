from sqlalchemy import Column, String, Float, ForeignKey
from .models import *

class PredictionTrendFundsModel(Base):
    __tablename__ = 'prediction_trend_funds'
    
    fund_name = Column(String(255), ForeignKey('mutual_funds.fund_name'), primary_key=True)
    date = Column(Date, primary_key=True)
    trend = Column(Integer)
    up_trend_prob = Column(Float)
    down_trend_prob = Column(Float)
    reason = Column(String(255))
    indicator = Column(String(255))