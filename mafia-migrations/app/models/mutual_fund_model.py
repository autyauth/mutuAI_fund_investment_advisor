from sqlalchemy import Column, String
from .models import *
class MutualFundModel(Base):
    __tablename__ = 'mutual_funds'
    
    fund_name = Column(String(255), primary_key=True)
    category = Column(String(255))
    securities_industry = Column(String(255))
    fund_type = Column(String(255))
    fund_risk = Column(String(255))
    dividend_policy = Column(String(255))
    redemption_fee = Column(Float)
    purchase_fee = Column(Float)
    fund_expense_ratio = Column(Float)
    minimum_initial_investment = Column(Integer)
    fund_registration_date = Column(Date)
    company = Column(String(255))
    fund_fact = Column(String(255))
    model_ml_info_path = Column(String(255))