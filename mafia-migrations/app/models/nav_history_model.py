from sqlalchemy import Column, String, Float, Date, ForeignKey, Numeric
from .models import *

class NavHistoryModel(Base):
    __tablename__ = 'nav_history'

    fund_name = Column(String(255), ForeignKey('mutual_funds.fund_name'), primary_key=True)
    date = Column(Date, primary_key=True)
    nav = Column(Numeric(10, 4))
    fund_type = Column(String(255))
    selling_price = Column(Numeric(10, 4))
    redemption_price = Column(Numeric(10, 4))
    total_net_assets = Column(Numeric(18, 2))
    change = Column(Float)