from typing import Dict, List
from services.exceptions import BusinessLogicException
from adapters.models import Deduction2025Model
import logging

class TaxDeduction2025Service:
    def __init__(self, deduction_repository, tax_repository, goal_repository):
        self.deduction_repository = deduction_repository
        self.tax_repository = tax_repository
        self.goal_repository = goal_repository
        self.logger = logging.getLogger(__name__)

    def _calculate_tax(self, taxable_income: float) -> float:
        """Calculate tax based on Thailand's tax brackets for 2025"""
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
            tax = bracket_income * rate
            total_tax += tax
            remaining_income -= bracket_income
            
        return total_tax

    def calculate_deductions(self, username: str, tax_input: dict) -> dict:
        try:
            # Calculate total income
            annual_income = tax_input.get('monthly_income', 0) * 12
            bonus_income = tax_input.get('bonus_income', 0)
            additional_income = tax_input.get('additional_income', 0)
            total_income = annual_income + bonus_income + additional_income
            # ค่าใช้จ่าย 50% ไม่เกิน 100,000 บาท
            total_income = total_income - (total_income * 0.5 if total_income * 0.5 <= 100000 else 100000)
            tax_input['taxable_income'] = max(total_income - 150_000, 0) 

            # Calculate all deductions
            deduction_breakdown = {}
            total_deduction = 0

            # 1. Personal deduction
            personal_deduction = 60000
            total_deduction += personal_deduction
            deduction_breakdown['personal_deduction'] = personal_deduction

            # 2. Marital deduction
            if tax_input.get('marital_status') in ['married', 'married_no_income']:
                marital_deduction = 60000
                total_deduction += marital_deduction
                deduction_breakdown['marital_deduction'] = marital_deduction

            # 3. Child deduction
            child_deduction = self._calculate_child_deduction(tax_input.get('children', []))
            total_deduction += child_deduction
            deduction_breakdown['child_deduction'] = child_deduction

            # 4. Parent deduction
            number_of_parents = min(tax_input.get('number_of_parents', 0), 4)
            parent_deduction = number_of_parents * 30000
            total_deduction += parent_deduction
            deduction_breakdown['parent_deduction'] = parent_deduction

            # 5. Disable deduction
            if tax_input.get('has_disabled_person'):
                disable_deduction = 60000
                total_deduction += disable_deduction
                deduction_breakdown['disable_deduction'] = disable_deduction

            # 6. Prenatal deduction
            prenatal_deduction = min(tax_input.get('prenatal_expense', 0), 60000)
            total_deduction += prenatal_deduction
            deduction_breakdown['prenatal_deduction'] = prenatal_deduction

            # 7-9. Life insurance deductions
            life_insurance = self._calculate_life_insurance_deductions(tax_input)
            total_deduction += life_insurance['total']
            deduction_breakdown.update(life_insurance['breakdown'])

            # 10-15. Fund deductions
            funds = self._calculate_fund_deductions(tax_input)
            total_deduction += funds['total']
            deduction_breakdown.update(funds['breakdown'])

            # 16-20. Other deductions
            others = self._calculate_other_deductions(tax_input)
            total_deduction += others['total']
            deduction_breakdown.update(others['breakdown'])

            # Calculate income after deductions for donations
            income_after_deductions = total_income - total_deduction

            # 21-22. Donations
            donations = self._calculate_donation_deductions(tax_input, income_after_deductions)
            total_deduction += donations['total']
            deduction_breakdown.update(donations['breakdown'])

            # Calculate final taxable income
            taxable_income = max(total_income - total_deduction, 0)

            # Calculate taxes
            tax_amount = self._calculate_tax(taxable_income)
            original_tax = self._calculate_tax(total_income)
            tax_saving = original_tax - tax_amount

            # Calculate fund deductions with remaining allowance
            fund_calculations = self._calculate_fund_deductions(tax_input)
            
            # Save to deduction table
            deduction_model = Deduction2025Model(
                username=username,
                year=2025,
                monthly_income=tax_input['monthly_income'],
                bonus_income=tax_input.get('bonus_income', 0),
                additional_income=tax_input.get('additional_income', 0),
                personal_deduction=personal_deduction,
                marital_deduction=deduction_breakdown.get('marital_deduction', 0),
                child_deduction=child_deduction,
                parent_deduction=parent_deduction,
                disable_deduction=deduction_breakdown.get('disable_deduction', 0),
                prenatal_deduction=prenatal_deduction,
                general_life_insurance=life_insurance['breakdown']['general_life_insurance'],
                parent_life_insurance=life_insurance['breakdown']['parent_life_insurance'],
                self_life_insurance=life_insurance['breakdown']['self_life_insurance'],
                provident_fund=fund_calculations['breakdown']['provident_fund'],
                pension_fund=fund_calculations['breakdown']['pension_fund'],
                rmf_fund=fund_calculations['breakdown']['rmf_fund'],
                pension_life_insurance=fund_calculations['breakdown']['pension_life_insurance'],
                national_saving_fund=fund_calculations['breakdown']['national_saving_fund'],
                housing_interest=others['breakdown']['housing_interest'],
                social_enterprise=others['breakdown']['social_enterprise'],
                thai_esg=others['breakdown']['thai_esg'],
                new_housing=others['breakdown']['new_housing'],
                easy_receipt=others['breakdown']['easy_receipt'],
                education_donation=donations['breakdown']['education_donation'],
                general_donation=donations['breakdown']['general_donation'],
                total_income=total_income,
                total_deduction=total_deduction,
                taxable_income=taxable_income
            )
            self.deduction_repository.save_deduction(deduction_model)

            # Save to tax table
            tax_data = {
                'username': username,
                'year': 2025,
                'users_tax': tax_amount
            }
            self.tax_repository.save_tax(tax_data)

            # Save to goal table (RMF remaining allowance)
            goal_data = {
                'username': username,
                'year': 2025,
                'users_goal': fund_calculations['rmf_remaining_allowance']
            }
            self.goal_repository.save_goal(goal_data)

            return {
                'income_breakdown': {
                    'annual_income': annual_income,
                    'bonus_income': bonus_income,
                    'additional_income': additional_income,
                    'total_income': total_income
                },
                'total_deduction': total_deduction,
                'taxable_income': taxable_income,
                'deduction_breakdown': deduction_breakdown,
                'tax_calculation': {
                    'original_tax': original_tax,
                    'final_tax': tax_amount,
                    'tax_saving': tax_saving
                },
                'fund_limits': {
                    'rmf_remaining_allowance': fund_calculations['rmf_remaining_allowance']
                }
            }

        except Exception as e:
            self.logger.error(f"Error calculating 2025 deductions: {str(e)}")
            raise BusinessLogicException(f"Failed to calculate deductions: {str(e)}")

    def _calculate_child_deduction(self, children: List[Dict]) -> float:
        total_deduction = 0
        adopted_count = 0

        for i, child in enumerate(children):
            if child.get('is_adopted'):
                if adopted_count < 3:
                    total_deduction += 30000
                    adopted_count += 1
                continue

            if i == 0:  # First child
                total_deduction += 30000
            else:  # Second and subsequent children
                if child.get('birth_after_2018'):
                    total_deduction += 60000
                else:
                    total_deduction += 30000

        return total_deduction

    def _calculate_life_insurance_deductions(self, tax_input: dict) -> dict:
        general_insurance = min(tax_input.get('general_life_insurance', 0), 100000)
        parent_insurance = min(tax_input.get('parent_life_insurance', 0), 15000)
        self_insurance = min(tax_input.get('self_life_insurance', 0), 25000)

        if general_insurance + self_insurance > 100000:
            self_insurance = max(0, 100000 - general_insurance)

        total = general_insurance + parent_insurance + self_insurance

        return {
            'total': total,
            'breakdown': {
                'general_life_insurance': general_insurance,
                'parent_life_insurance': parent_insurance,
                'self_life_insurance': self_insurance
            }
        }

    def _calculate_fund_deductions(self, tax_input: dict) -> dict:
        """Calculate fund-based deductions with specific Thai tax rules"""
        monthly_income = tax_input.get('monthly_income', 0)
        taxable_income = tax_input.get('taxable_income', 0)

        # 1. Pension Fund: Not exceeding 15% of salary
        max_pension = monthly_income * 12 * 0.15
        pension = min(max_pension, tax_input.get('pension_fund', 0))

        # 2. RMF: Not exceeding 30% of taxable income
        max_rmf = taxable_income * 0.30
        rmf = min(max_rmf, tax_input.get('rmf_fund', 0))

        # 3. Pension Life Insurance: Not exceeding 15% of taxable income and not exceeding 200,000
        max_pension_insurance = min(taxable_income * 0.15, 200000)
        pension_insurance = min(max_pension_insurance, tax_input.get('pension_life_insurance', 0))

        # 4. National Saving Fund: Not exceeding 30,000
        nsf = min(tax_input.get('national_saving_fund', 0), 30000)

        # Calculate total and adjust if exceeds 500,000
        total = pension + rmf + pension_insurance + nsf
        
        if total > 500000:
            # Proportionally reduce each component
            reduction_ratio = 500000 / total
            pension *= reduction_ratio
            rmf *= reduction_ratio
            pension_insurance *= reduction_ratio
            nsf *= reduction_ratio
            total = 500000

        # Calculate remaining RMF allowance for goal
        current_fund_total = pension + rmf + pension_insurance + nsf
        remaining_allowance = min(
            500000 - current_fund_total,  # Overall limit remaining
            max_rmf - rmf  # RMF-specific limit remaining
        )

        return {
            'total': total,
            'breakdown': {
                'provident_fund': pension,
                'pension_fund': pension,
                'rmf_fund': rmf,
                'pension_life_insurance': pension_insurance,
                'national_saving_fund': nsf
            },
            'rmf_remaining_allowance': remaining_allowance
        }

    def _calculate_other_deductions(self, tax_input: dict) -> dict:
        housing_interest = min(tax_input.get('housing_interest', 0), 100000)
        social_enterprise = min(tax_input.get('social_enterprise', 0), 100000)
        
        thai_esg = min(
            tax_input.get('thai_esg', 0),
            tax_input.get('taxable_income', 0) * 0.30,
            300000
        )

        house_cost = tax_input.get('new_house_cost', 0)
        new_housing = min((house_cost // 1000000) * 10000, 100000)
        easy_receipt = min(tax_input.get('easy_receipt', 0), 50000)

        total = housing_interest + social_enterprise + thai_esg + new_housing + easy_receipt

        return {
            'total': total,
            'breakdown': {
                'housing_interest': housing_interest,
                'social_enterprise': social_enterprise,
                'thai_esg': thai_esg,
                'new_housing': new_housing,
                'easy_receipt': easy_receipt
            }
        }

    def _calculate_donation_deductions(self, tax_input: dict, income_after_deductions: float) -> dict:
        education_limit = income_after_deductions * 0.10
        education_donation = max(min(tax_input.get('education_donation', 0) * 2, education_limit), 0)

        income_after_edu = income_after_deductions - education_donation
        general_limit = income_after_edu * 0.10
        general_donation =max(min(tax_input.get('general_donation', 0), general_limit),0)

        total = education_donation + general_donation

        return {
            'total': total,
            'breakdown': {
                'education_donation': education_donation,
                'general_donation': general_donation
            }
        }