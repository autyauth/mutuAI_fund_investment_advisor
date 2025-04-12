from sqlalchemy import Column, String, Float, Date, Integer, DECIMAL
from .models import *

class UserTokenModel(Base):
    __tablename__ = 'user_tokens'
    
    username = Column(String(255), primary_key=True)
    token = Column(String(512), primary_key=True)
    expires_at = Column(Date)
