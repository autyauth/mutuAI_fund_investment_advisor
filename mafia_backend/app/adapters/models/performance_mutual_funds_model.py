from sqlalchemy import Column, String, Float, ForeignKey
from .models import *

class PerformanceMutualFundsModel(Base):
    __tablename__ = 'perfomance_mutual_funds'
    
    fund_name = Column(String(255), ForeignKey('mutual_funds.fund_name'), primary_key=True)
    date = Column(Date, primary_key=True)
    std_three_month = Column(Float)
    std_six_month = Column(Float)
    std_one_year = Column(Float)
    std_three_year = Column(Float)
    std_five_year = Column(Float)
    std_ten_year = Column(Float)
    sharpe_ratio_three_month = Column(Float)
    sharpe_ratio_six_month = Column(Float)
    sharpe_ratio_one_year = Column(Float)
    sharpe_ratio_three_year = Column(Float)
    sharpe_ratio_five_year = Column(Float)
    sharpe_ratio_ten_year = Column(Float)
