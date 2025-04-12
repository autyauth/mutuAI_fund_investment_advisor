from sqlalchemy import Column, String, Float, Integer, ForeignKey, DECIMAL
from .models import *
class GoalModel(Base):
    __tablename__ = 'goal'
    username = Column(String(255), ForeignKey('users.username'), primary_key=True)
    year = Column(Integer, primary_key=True)
    users_goal = Column(DECIMAL(10, 2))
    rate_fund = Column(DECIMAL(10, 4))
    std_fund = Column(DECIMAL(10, 4))
    rmf_amount_invested = Column(DECIMAL(10, 2), nullable=True)
    ssf_amount_invested = Column(DECIMAL(10, 2), nullable=True)
    thaiesg_amount_invested = Column(DECIMAL(10, 2), nullable=True)