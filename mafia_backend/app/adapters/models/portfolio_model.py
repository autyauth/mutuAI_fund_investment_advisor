from sqlalchemy import Column, String, Float, ForeignKey, DECIMAL
from .models import *

class PortfolioModel(Base):
    __tablename__ = 'portfolio'
    username = Column(String(255), ForeignKey('users.username'), primary_key=True)
    fund_name = Column(String(255), primary_key=True)
    fund_type = Column(String(255))
    gain_loss_percent = Column(DECIMAL(10, 2))
    gain_loss_value = Column(DECIMAL(10, 2))
    holding_units = Column(DECIMAL(10, 4))
    holding_value = Column(DECIMAL(10, 2))
    cost = Column(DECIMAL(10, 2))
    total_profit = Column(DECIMAL(10, 2))
    nav_average = Column(DECIMAL(10, 4))
    present_nav = Column(DECIMAL(10, 4))
    valid_units = Column(DECIMAL(10, 4))