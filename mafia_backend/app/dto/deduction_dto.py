from adapters.models.deduction_model import DeductionModel

class DeductionDTO:
    def __init__(self, username: str, year: int, users_deduction: float, monthly_income: float, bonus: float, other_income: float, marital_status: str, num_children: int, num_parents: int, num_disabled_dependents: int, social_security: float, life_insurance: float, health_insurance: float, parent_health_insurance: float, social_enterprise: float, thai_esg: float, rmf: float, ssf: float, pvd: float, gpf: float, nsf: float, pension_insurance: float, general_donation: float, education_donation: float, political_donation: float, easy_receipt: float, secondary_tourism: float, mortgage_interest: float, new_house_cost: float, pregnancy_expense: float):
        self.username = username
        self.year = year
        self.users_deduction = users_deduction
        self.monthly_income = monthly_income
        self.bonus = bonus
        self.other_income = other_income
        self.marital_status = marital_status
        self.num_children = num_children
        self.num_parents = num_parents
        self.num_disabled_dependents = num_disabled_dependents
        self.social_security = social_security
        self.life_insurance = life_insurance
        self.health_insurance = health_insurance
        self.parent_health_insurance = parent_health_insurance
        self.social_enterprise = social_enterprise
        self.thai_esg = thai_esg
        self.rmf = rmf
        self.ssf = ssf
        self.pvd = pvd
        self.gpf = gpf
        self.nsf = nsf
        self.pension_insurance = pension_insurance
        self.general_donation = general_donation
        self.education_donation = education_donation
        self.political_donation = political_donation
        self.easy_receipt = easy_receipt
        self.secondary_tourism = secondary_tourism
        self.mortgage_interest = mortgage_interest
        self.new_house_cost = new_house_cost
        self.pregnancy_expense = pregnancy_expense
        
    def to_dict(self):
        return {
            'username': self.username,
            'year': self.year,
            'users_deduction': self.users_deduction,
            'monthly_income': self.monthly_income,
            'bonus': self.bonus,
            'other_income': self.other_income,
            'marital_status': self.marital_status,
            'num_children': self.num_children,
            'num_parents': self.num_parents,
            'num_disabled_dependents': self.num_disabled_dependents,
            'social_security': self.social_security,
            'life_insurance': self.life_insurance,
            'health_insurance': self.health_insurance,
            'parent_health_insurance': self.parent_health_insurance,
            'social_enterprise': self.social_enterprise,
            'thai_esg': self.thai_esg,
            'rmf': self.rmf,
            'ssf': self.ssf,
            'pvd': self.pvd,
            'gpf': self.gpf,
            'nsf': self.nsf,
            'pension_insurance': self.pension_insurance,
            'general_donation': self.general_donation,
            'education_donation': self.education_donation,
            'political_donation': self.political_donation,
            'easy_receipt': self.easy_receipt,
            'secondary_tourism': self.secondary_tourism,
            'mortgage_interest': self.mortgage_interest,
            'new_house_cost': self.new_house_cost,
            'pregnancy_expense': self.pregnancy_expense
        }
    
    @staticmethod
    def from_model(deduction: DeductionModel):
        return DeductionDTO(
            username=deduction.username,
            year=deduction.year,
            users_deduction=deduction.users_deduction,
            monthly_income=deduction.monthly_income,
            bonus=deduction.bonus,
            other_income=deduction.other_income,
            marital_status=deduction.marital_status,
            num_children=deduction.num_children,
            num_parents=deduction.num_parents,
            num_disabled_dependents=deduction.num_disabled_dependents,
            social_security=deduction.social_security,
            life_insurance=deduction.life_insurance,
            health_insurance=deduction.health_insurance,
            parent_health_insurance=deduction.parent_health_insurance,
            social_enterprise=deduction.social_enterprise,
            thai_esg=deduction.thai_esg,
            rmf=deduction.rmf,
            ssf=deduction.ssf,
            pvd=deduction.pvd,
            gpf=deduction.gpf,
            nsf=deduction.nsf,
            pension_insurance=deduction.pension_insurance,
            general_donation=deduction.general_donation,
            education_donation=deduction.education_donation,
            political_donation=deduction.political_donation,
            easy_receipt=deduction.easy_receipt,
            secondary_tourism=deduction.secondary_tourism,
            mortgage_interest=deduction.mortgage_interest,
            new_house_cost=deduction.new_house_cost,
            pregnancy_expense=deduction.pregnancy_expense
        )