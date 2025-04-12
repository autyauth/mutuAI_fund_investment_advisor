from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.auth_utils import user_access_required
from services.tax_service import TaxService
from services.deduction_service import DeductionService
from dto.tax_dto import TaxCalculationDto, MaritalStatus
import logging

def create_deduction_bp(deduction_service: DeductionService):
    bp = Blueprint('deduction', __name__, url_prefix='/api/deduction')
    logger = logging.getLogger(__name__)
    
    @bp.route('/<username>/<int:year>', methods=['GET'])
    @jwt_required()
    @user_access_required
    def get_deduction(username: str, year: int):
        try:
            deduction = None
            if year <= 2024:
                deduction = deduction_service.get_deduction(username, year) 
            elif year >= 2025:
                deduction = deduction_service.get_deduct_2025(username, year)
            return jsonify(deduction), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    

    return bp

   