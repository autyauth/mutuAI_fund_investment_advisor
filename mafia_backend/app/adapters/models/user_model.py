from sqlalchemy import Column, String, Float, Date, Integer, DECIMAL
from .models import *
class UserModel(Base):
    __tablename__ = 'users'
    
    username = Column(String(255), primary_key=True)
    password = Column(String(255), nullable=False)
    email = Column(String(255))
    telephone_number = Column(String(255))
    birthday = Column(Date)
    job = Column(String(255))
    salary = Column(DECIMAL(10, 2))
    risk_level = Column(Integer)