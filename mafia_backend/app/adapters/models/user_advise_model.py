from sqlalchemy import Column, String, Integer, ForeignKey

from .models import *
class UserAdviseModel(Base):
    __tablename__ = "user_advise"

    username = Column(String(255), ForeignKey("users.username", ondelete="CASCADE"), primary_key=True)
    year = Column(Integer, nullable=False, primary_key=True)
    fund_name = Column(String(255), ForeignKey("mutual_funds.fund_name", ondelete="CASCADE"), nullable=False, primary_key=True)
    is_deleted = Column(Boolean, nullable=False, default=False)
