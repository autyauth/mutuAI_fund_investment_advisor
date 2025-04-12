from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.auth_utils import user_access_required
from services.tax_service import TaxService
from services.deduction_service import DeductionService
from dto.tax_dto import TaxCalculationDto, MaritalStatus
import logging

def create_tax_bp(tax_service: TaxService):
    bp = Blueprint('tax', __name__, url_prefix='/api/tax')
    logger = logging.getLogger(__name__)

    @bp.route('/user/<username>', methods=['GET'])
    @jwt_required()
    @user_access_required
    def get_user_tax_history(username: str):
        try:
            tax_history = tax_service.get_tax_history_by_username(username)
            return jsonify(tax_history), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    @bp.route('/user/<username>/<int:year>', methods=['GET'])
    @jwt_required()
    @user_access_required
    def get_user_tax_history_year(username: str, year: int):
        try:
            tax_history = tax_service.get_tax_history_by_username_year(username, year)
            return jsonify(tax_history), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @bp.route('/calculate/<username>/<int:year>', methods=['POST'])
    @jwt_required()
    @user_access_required
    def calculate_tax(username: str, year: int):
        try:
            
            data = request.get_json()
            tax_input = TaxCalculationDto(
                monthly_income=float(data.get('monthly_income', 0)),
                bonus=float(data.get('bonus', 0)),
                other_income=float(data.get('other_income', 0)),
                marital_status=MaritalStatus(data.get('marital_status', 'single')),
                num_children=int(data.get('num_children', 0)),
                num_parents=int(data.get('num_parents', 0)),
                num_disabled_dependents=int(data.get('num_disabled_dependents', 0)),
                social_security=float(data.get('social_security', 0)),
                life_insurance=float(data.get('life_insurance', 0)),
                health_insurance=float(data.get('health_insurance', 0)),
                parent_health_insurance=float(data.get('parent_health_insurance', 0)),
                social_enterprise=float(data.get('social_enterprise', 0)),
                thai_esg=float(data.get('thai_esg', 0)),
                rmf=float(data.get('rmf', 0)),
                ssf=float(data.get('ssf', 0)),
                pvd=float(data.get('pvd', 0)),
                gpf=float(data.get('gpf', 0)),
                nsf=float(data.get('nsf', 0)),
                pension_insurance=float(data.get('pension_insurance', 0)),
                general_donation=float(data.get('general_donation', 0)),
                education_donation=float(data.get('education_donation', 0)),
                political_donation=float(data.get('political_donation', 0)),
                easy_receipt=float(data.get('easy_receipt', 0)),
                secondary_tourism=float(data.get('secondary_tourism', 0)),
                mortgage_interest=float(data.get('mortgage_interest', 0)),
                new_house_cost=float(data.get('new_house_cost', 0)),
                pregnancy_expense=float(data.get('pregnancy_expense', 0))
            )
            logger.debug(f"Calculating tax for user {username} with input: {tax_input}")
            
            result = tax_service.calculate_tax(tax_input, username, year)
            return jsonify(result), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return bp

   