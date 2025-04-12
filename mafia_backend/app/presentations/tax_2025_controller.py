from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from utils.auth_utils import user_access_required
from services.tax_2025_service import TaxDeduction2025Service
import logging

def create_tax_2025_bp(tax_2025_service: TaxDeduction2025Service):
    bp = Blueprint('tax_2025', __name__, url_prefix='/api/tax-2025')
    logger = logging.getLogger(__name__)

    @bp.route('/calculate/<username>', methods=['POST'])
    @jwt_required()
    @user_access_required
    def calculate_tax_2025(username: str):
        try:
            data = request.get_json()
            logger.info(f"Calculating 2025 tax deductions for user: {username}")

            required_fields = ['monthly_income', 'bonus_income', 'additional_income', 'marital_status']
            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"Missing required field: {field}"}), 400

            children = data.get('children', [])
            if not isinstance(children, list):
                return jsonify({"error": "Children must be a list"}), 400
            
            for child in children:
                if not isinstance(child, dict):
                    return jsonify({"error": "Each child must be an object"}), 400
                if 'birth_after_2018' not in child:
                    return jsonify({"error": "Each child must specify birth_after_2018"}), 400
                if 'is_adopted' not in child:
                    return jsonify({"error": "Each child must specify is_adopted"}), 400

            numeric_fields = [
                'monthly_income', 'bonus_income', 'additional_income', 'number_of_parents',
                'prenatal_expense', 'general_life_insurance', 'parent_life_insurance',
                'self_life_insurance', 'provident_fund', 'pension_fund', 'rmf_fund',
                'pension_life_insurance', 'national_saving_fund', 'housing_interest',
                'social_enterprise', 'thai_esg', 'new_house_cost', 'easy_receipt',
                'education_donation', 'general_donation'
            ]

            for field in numeric_fields:
                if field in data and not isinstance(data[field], (int, float)):
                    return jsonify({"error": f"Field {field} must be a number"}), 400
                if field in data and data[field] < 0:
                    return jsonify({"error": f"Field {field} must be non-negative"}), 400

            result = tax_2025_service.calculate_deductions(username, data)
            
            response = {
                "input": {
                    "username": username,
                    "monthly_income": data.get('monthly_income'),
                    "bonus_income": data.get('bonus_income'),
                    "additional_income": data.get('additional_income'),
                    "marital_status": data.get('marital_status'),
                    "number_of_children": len(children),
                    "number_of_parents": data.get('number_of_parents', 0)
                },
                "calculations": result
            }

            return jsonify(response), 200

        except ValueError as e:
            logger.error(f"Validation error: {str(e)}")
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error(f"Error calculating 2025 tax: {str(e)}")
            return jsonify({"error": str(e)}), 500

    return bp