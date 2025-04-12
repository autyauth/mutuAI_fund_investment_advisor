from adapters.repositories.tax_repository import TaxRepository
from dto.tax_dto import TaxCalculationDto, MaritalStatus

class TaxService:
    def __init__(self, tax_repository: TaxRepository):
        self.tax_repository = tax_repository

    def calculate_tax(self, tax_input: TaxCalculationDto, username: str, year: int):
        # Calculate total income
        total_income = self._calculate_total_income(tax_input)

        # Calculate deductions
        total_deductions = self._calculate_total_deductions(tax_input)

        # Calculate taxable income
        taxable_income = max(total_income - total_deductions, 0)

        # Calculate tax
        tax_amount = self._calculate_tax_amount(taxable_income)
        
        deductions = {
            'total_deductions': total_deductions,
            'monthly_income': tax_input.monthly_income,
            'bonus': tax_input.bonus,
            'other_income': tax_input.other_income,
            'marital_status': tax_input.marital_status.name if isinstance(tax_input.marital_status, MaritalStatus) else tax_input.marital_status,
            'num_children': tax_input.num_children,
            'num_parents': tax_input.num_parents,
            'num_disabled_dependents': tax_input.num_disabled_dependents,
            'social_security': tax_input.social_security,
            'life_insurance': tax_input.life_insurance,
            'health_insurance': tax_input.health_insurance,
            'parent_health_insurance': tax_input.parent_health_insurance,
            'social_enterprise': tax_input.social_enterprise,
            'thai_esg': tax_input.thai_esg,
            'rmf': tax_input.rmf,
            'ssf': tax_input.ssf,
            'pvd': tax_input.pvd,
            'gpf': tax_input.gpf,
            'nsf': tax_input.nsf,
            'pension_insurance': tax_input.pension_insurance,
            'general_donation': tax_input.general_donation,
            'education_donation': tax_input.education_donation,
            'political_donation': tax_input.political_donation,
            'easy_receipt': tax_input.easy_receipt,
            'secondary_tourism': tax_input.secondary_tourism,
            'mortgage_interest': tax_input.mortgage_interest,
            'new_house_cost': tax_input.new_house_cost,
            'pregnancy_expense': tax_input.pregnancy_expense
        }
        # Save to database
        self.tax_repository.save_tax(username, year, tax_amount)
        self.tax_repository.save_deduction(username, year, deductions)

        return {
            'total_income': total_income,
            'total_deductions': total_deductions,
            'taxable_income': taxable_income,
            'tax_amount': tax_amount,
            'deductions_breakdown': self._get_deductions_breakdown(tax_input)
        }

    def _calculate_total_income(self, tax_input: TaxCalculationDto) -> float:
        return round((tax_input.monthly_income * 12) + tax_input.bonus + tax_input.other_income, 2)

    def _calculate_expense_deduction(self, tax_input: TaxCalculationDto) -> float:
        total_income = self._calculate_total_income(tax_input)
        return round(min(total_income * 0.5, 100000), 2)

    def _calculate_personal_deduction(self, tax_input: TaxCalculationDto) -> float:
        deduction = 60000
        if tax_input.marital_status == MaritalStatus.SPOUSE_WITHOUT_INCOME:
            deduction += 60000
        return deduction

    def _calculate_dependent_deduction(self, tax_input: TaxCalculationDto) -> float:
        children_deduction = tax_input.num_children * 30000
        parent_deduction = min(tax_input.num_parents * 30000, 120000)
        disabled_deduction = tax_input.num_disabled_dependents * 60000
        return children_deduction + parent_deduction + disabled_deduction

    def _calculate_insurance_deduction(self, tax_input: TaxCalculationDto) -> float:
        social_security = min(tax_input.social_security, 9000)
        life_health_combined = min(
            tax_input.life_insurance + tax_input.health_insurance,
            100000
        )
        parent_health = min(tax_input.parent_health_insurance, 15000)
        return social_security + life_health_combined + parent_health

    def _calculate_investment_deduction(self, tax_input: TaxCalculationDto) -> float:
        total_income = self._calculate_total_income(tax_input)
        max_percent = total_income * 0.3  # 30% of total income
        
        social_enterprise = min(tax_input.social_enterprise, 100000)
        thai_esg = min(tax_input.thai_esg, max_percent, 300000)
        
        # Combined retirement investments cannot exceed 500,000
        retirement_investments = [
            min(tax_input.rmf, max_percent),
            min(tax_input.ssf, max_percent),
            min(tax_input.pvd, total_income * 0.15),
            tax_input.gpf,
            tax_input.nsf,
            min(tax_input.pension_insurance, total_income * 0.15)
        ]
        retirement_total = min(sum(retirement_investments), 500000)
        
        return round(social_enterprise + thai_esg + retirement_total, 2)

    def _calculate_donation_deduction(self, tax_input: TaxCalculationDto) -> float:
        base_deductions = sum([
            self._calculate_expense_deduction(tax_input),
            self._calculate_personal_deduction(tax_input),
            self._calculate_dependent_deduction(tax_input),
            self._calculate_insurance_deduction(tax_input),
            self._calculate_investment_deduction(tax_input),
            self._calculate_special_deductions(tax_input)
        ])
        # income_after_deductions = self._calculate_total_income(tax_input) - base_deductions
        # max_donation = income_after_deductions * 0.1
        
        # ป้องกัน income_after_deductions ติดลบ
        income_after_deductions = max(self._calculate_total_income(tax_input) - base_deductions, 0)
        
        # ป้องกัน max_donation ติดลบ
        max_donation = max(income_after_deductions * 0.1, 0)
        
        general = min(tax_input.general_donation, max_donation)
        education = min(tax_input.education_donation * 2, max_donation)
        political = min(tax_input.political_donation, 10000)
        
        return round(general + education + political, 2)

    def _calculate_special_deductions(self, tax_input: TaxCalculationDto) -> float:
        easy_receipt = min(tax_input.easy_receipt, 50000)
        tourism = min(tax_input.secondary_tourism, 15000)
        mortgage = min(tax_input.mortgage_interest, 100000)
        house_deduction = min((tax_input.new_house_cost // 1000000) * 10000, 100000)
        pregnancy = min(tax_input.pregnancy_expense, 60000)
        
        return easy_receipt + tourism + mortgage + house_deduction + pregnancy

    def _calculate_total_deductions(self, tax_input: TaxCalculationDto) -> float:
        return sum([
            self._calculate_expense_deduction(tax_input),
            self._calculate_personal_deduction(tax_input),
            self._calculate_dependent_deduction(tax_input),
            self._calculate_insurance_deduction(tax_input),
            self._calculate_investment_deduction(tax_input),
            self._calculate_donation_deduction(tax_input),
            self._calculate_special_deductions(tax_input)
        ])

    def _calculate_tax_amount(self, taxable_income: float) -> float:
        tax_brackets = [
            (0, 150000, 0),
            (150001, 300000, 0.05),
            (300001, 500000, 0.10),
            (500001, 750000, 0.15),
            (750001, 1000000, 0.20),
            (1000001, 2000000, 0.25),
            (2000001, 5000000, 0.30),
            (5000001, float('inf'), 0.35)
        ]
        
        total_tax = 0
        remaining_income = taxable_income
        
        for min_income, max_income, rate in tax_brackets:
            if remaining_income <= 0:
                break
            bracket_income = min(remaining_income, max_income - min_income + 1)
            total_tax += bracket_income * rate
            remaining_income -= bracket_income
        
        return round(total_tax, 2)

    def _get_deductions_breakdown(self, tax_input: TaxCalculationDto) -> dict:
        return {
            'expense': self._calculate_expense_deduction(tax_input),
            'personal': self._calculate_personal_deduction(tax_input),
            'dependent': self._calculate_dependent_deduction(tax_input),
            'insurance': self._calculate_insurance_deduction(tax_input),
            'investment': self._calculate_investment_deduction(tax_input),
            'donation': self._calculate_donation_deduction(tax_input),
            'special': self._calculate_special_deductions(tax_input)
        }

    def get_tax_history_by_username(self, username: str):
        tax_records = self.tax_repository.get_tax_by_username(username)
        if not tax_records or len(tax_records) == 0:
            return []
        return [self._tax_to_dto(tx) for tx in tax_records]
    
    def get_tax_history_by_username_year(self, username: str, year: int):
        tax_record = self.tax_repository.get_tax_by_username_year(username, year)
        if not tax_record:
            return None
        return self._tax_to_dto(tax_record)

    def _tax_to_dto(self, tax):
        return {
            'year': tax.year,
            'users_tax': float(tax.users_tax)
    }