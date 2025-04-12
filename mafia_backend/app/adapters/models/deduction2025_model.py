from sqlalchemy import Column, String, Float, Integer, ForeignKey, DECIMAL
from .models import *
class Deduction2025Model(Base):
    __tablename__ = 'deduction_2025'
    
    username = Column(String(255), ForeignKey('users.username', ondelete='CASCADE'), primary_key=True)
    year = Column(Integer, primary_key=True)
    monthly_income = Column(DECIMAL(10,2))
    bonus_income = Column(DECIMAL(10,2))
    additional_income = Column(DECIMAL(10,2))
    personal_deduction = Column(DECIMAL(10,2))
    marital_deduction = Column(DECIMAL(10,2))
    child_deduction = Column(DECIMAL(10,2))
    parent_deduction = Column(DECIMAL(10,2))
    disable_deduction = Column(DECIMAL(10,2))
    prenatal_deduction = Column(DECIMAL(10,2))
    general_life_insurance = Column(DECIMAL(10,2))
    parent_life_insurance = Column(DECIMAL(10,2))
    self_life_insurance = Column(DECIMAL(10,2))
    provident_fund = Column(DECIMAL(10,2))
    pension_fund = Column(DECIMAL(10,2))
    rmf_fund = Column(DECIMAL(10,2))
    pension_life_insurance = Column(DECIMAL(10,2))
    national_saving_fund = Column(DECIMAL(10,2))
    housing_interest = Column(DECIMAL(10,2))
    social_enterprise = Column(DECIMAL(10,2))
    thai_esg = Column(DECIMAL(10,2))
    new_housing = Column(DECIMAL(10,2))
    easy_receipt = Column(DECIMAL(10,2))
    education_donation = Column(DECIMAL(10,2))
    general_donation = Column(DECIMAL(10,2))
    total_income = Column(DECIMAL(10,2))
    total_deduction = Column(DECIMAL(10,2))
    taxable_income = Column(DECIMAL(10,2))

    def __repr__(self):
        return f"<Deduction2025(username={self.username}, year={self.year})>"