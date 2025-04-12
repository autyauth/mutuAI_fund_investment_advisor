from adapters.models.deduction2025_model import Deduction2025Model

class Deduction2025DTO:
    def __init__(self, username, year, monthly_income, bonus_income, additional_income, personal_deduction, marital_deduction, child_deduction, parent_deduction, disable_deduction, prenatal_deduction, general_life_insurance, parent_life_insurance, self_life_insurance, provident_fund, pension_fund, rmf_fund, pension_life_insurance, national_saving_fund, housing_interest, social_enterprise, thai_esg, new_housing, easy_receipt, education_donation, general_donation, total_income, total_deduction, taxable_income):
        self.username = username
        self.year = year
        self.monthly_income = monthly_income
        self.bonus_income = bonus_income
        self.additional_income = additional_income
        self.personal_deduction = personal_deduction
        self.marital_deduction = marital_deduction
        self.child_deduction = child_deduction
        self.parent_deduction = parent_deduction
        self.disable_deduction = disable_deduction
        self.prenatal_deduction = prenatal_deduction
        self.general_life_insurance = general_life_insurance
        self.parent_life_insurance = parent_life_insurance
        self.self_life_insurance = self_life_insurance
        self.provident_fund = provident_fund
        self.pension_fund = pension_fund
        self.rmf_fund = rmf_fund
        self.pension_life_insurance = pension_life_insurance
        self.national_saving_fund = national_saving_fund
        self.housing_interest = housing_interest
        self.social_enterprise = social_enterprise
        self.thai_esg = thai_esg
        self.new_housing = new_housing
        self.easy_receipt = easy_receipt
        self.education_donation = education_donation
        self.general_donation = general_donation
        self.total_income = total_income
        self.total_deduction = total_deduction
        self.taxable_income = taxable_income
    
    def to_dict(self):
        return {
            'username': self.username,
            'year': self.year,
            'monthly_income': self.monthly_income,
            'bonus_income': self.bonus_income,
            'additional_income': self.additional_income,
            'personal_deduction': self.personal_deduction,
            'marital_deduction': self.marital_deduction,
            'child_deduction': self.child_deduction,
            'parent_deduction': self.parent_deduction,
            'disable_deduction': self.disable_deduction,
            'prenatal_deduction': self.prenatal_deduction,
            'general_life_insurance': self.general_life_insurance,
            'parent_life_insurance': self.parent_life_insurance,
            'self_life_insurance': self.self_life_insurance,
            'provident_fund': self.provident_fund,
            'pension_fund': self.pension_fund,
            'rmf_fund': self.rmf_fund,
            'pension_life_insurance': self.pension_life_insurance,
            'national_saving_fund': self.national_saving_fund,
            'housing_interest': self.housing_interest,
            'social_enterprise': self.social_enterprise,
            'thai_esg': self.thai_esg,
            'new_housing': self.new_housing,
            'easy_receipt': self.easy_receipt,
            'education_donation': self.education_donation,
            'general_donation': self.general_donation,
            'total_income': self.total_income,
            'total_deduction': self.total_deduction,
            'taxable_income': self.taxable_income
        }
        
    @staticmethod
    def from_model(deduction: Deduction2025Model):
        return Deduction2025DTO(
            deduction.username,
            deduction.year,
            deduction.monthly_income,
            deduction.bonus_income,
            deduction.additional_income,
            deduction.personal_deduction,
            deduction.marital_deduction,
            deduction.child_deduction,
            deduction.parent_deduction,
            deduction.disable_deduction,
            deduction.prenatal_deduction,
            deduction.general_life_insurance,
            deduction.parent_life_insurance,
            deduction.self_life_insurance,
            deduction.provident_fund,
            deduction.pension_fund,
            deduction.rmf_fund,
            deduction.pension_life_insurance,
            deduction.national_saving_fund,
            deduction.housing_interest,
            deduction.social_enterprise,
            deduction.thai_esg,
            deduction.new_housing,
            deduction.easy_receipt,
            deduction.education_donation,
            deduction.general_donation,
            deduction.total_income,
            deduction.total_deduction,
            deduction.taxable_income
        )