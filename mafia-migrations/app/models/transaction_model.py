from sqlalchemy import Column, String, Float, Date, Integer, ForeignKey, DECIMAL
from .models import *

class TransactionModel(Base):
    __tablename__ = 'transactions'
    transaction_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), ForeignKey('users.username'))
    fund_name = Column(String(255), ForeignKey('mutual_funds.fund_name'))
    transaction_type = Column(Integer)
    transaction_date = Column(Date)
    units_processed = Column(DECIMAL(10, 4))
    amount_processed = Column(DECIMAL(10, 2))
    valid_to_sell = Column(Date)
    processed_nav = Column(DECIMAL(10, 4))
    gain_loss_percent = Column(DECIMAL(10, 2))
    gain_loss_value = Column(DECIMAL(10, 2))
    changed_gl_percent = Column(DECIMAL(10, 2))