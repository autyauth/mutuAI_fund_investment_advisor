from sqlalchemy import Column, Integer, String, DECIMAL, Float, ForeignKey, Date, TIMESTAMP, func
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.orm import relationship
from .models import *

class NotificationModel(Base):
    __tablename__ = "notifications"

    username = Column(
        String(255),
        ForeignKey("users.username"),
        primary_key=True,
        nullable=False
    )
    
    message = Column(
        String(255),
        primary_key=True,
        nullable=False
    )
    
    timestamp = Column(
        TIMESTAMP,
        nullable=False,
        server_default=func.now(),
        onupdate="CURRENT_TIMESTAMP"
    )
    
    is_read = Column(
        Integer,
        nullable=True,
        server_default=None
    )