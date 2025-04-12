from dataclasses import dataclass
from enum import Enum

class MaritalStatus(Enum):
    SINGLE = "single"
    DIVORCED = "divorced"
    SPOUSE_WITH_INCOME = "spouse_with_income"
    SPOUSE_WITHOUT_INCOME = "spouse_without_income"

@dataclass
class TaxCalculationDto:
    monthly_income: float
    bonus: float
    other_income: float
    marital_status: MaritalStatus
    num_children: int
    num_parents: int
    num_disabled_dependents: int
    social_security: float
    life_insurance: float
    health_insurance: float
    parent_health_insurance: float
    social_enterprise: float
    thai_esg: float
    rmf: float
    ssf: float
    pvd: float
    gpf: float
    nsf: float
    pension_insurance: float
    general_donation: float
    education_donation: float
    political_donation: float
    easy_receipt: float
    secondary_tourism: float
    mortgage_interest: float
    new_house_cost: float
    pregnancy_expense: float