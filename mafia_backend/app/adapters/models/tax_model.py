from sqlalchemy import Column, String, Float, Integer, ForeignKey, DECIMAL
from .models import *

class TaxModel(Base):
    __tablename__ = 'tax'
    username = Column(String(255), ForeignKey('users.username'), primary_key=True)
    year = Column(Integer, primary_key=True)
    users_tax = Column(DECIMAL(10, 2))