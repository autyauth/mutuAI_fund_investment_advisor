from flask import Blueprint, request, jsonify
from datetime import datetime
import logging

from adapters.exceptions import RecordNotFoundException
from services.performance_mutual_funds_service import PerformanceMutualFundsService
from flask_jwt_extended import jwt_required
from utils.auth_utils import user_access_required
def create_performance_mutual_funds_bp(performance_mutual_funds_service: PerformanceMutualFundsService):
    bp = Blueprint('performance-mutual-funds', __name__, url_prefix='/api/performance-mutual-funds')
    logger = logging.getLogger(__name__)

    @bp.route('/lastest/<fund_name>', methods=['GET'])
    def get_performance_by_fund(fund_name: str):
        try:
            if not fund_name:
                raise ValueError("Missing required query parameter: fund_name")
            logger.info(f"Getting performance for fund: {fund_name}")
            dto = performance_mutual_funds_service.get_performance_mutual_funds_lastest(fund_name)
            # change to % if data is float
            return jsonify(dto), 200
        except RecordNotFoundException as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            logger.error(f"Error getting performance by fund: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @bp.route('/all-with-risk', methods=['GET'])
    def get_performance_all_with_risk():
        try:
            logger.info("Getting home recommend funds")
            funds = performance_mutual_funds_service.get_home_recommend_funds()
            return jsonify(funds), 200
        except Exception as e:
            logger.error(f"Error getting home recommend funds: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @bp.route('/recommend/user/<username>', methods=['GET'])
    @jwt_required()
    @user_access_required
    def get_recommend_funds(username: str):
        try:
            logger.info("Getting home recommend funds")
            funds = performance_mutual_funds_service.reccoment_funds_with_user_risk_and_rate(username=username)
            return jsonify(funds), 200
        except Exception as e:
            logger.error(f"Error getting home recommend funds: {str(e)}")
            return jsonify({"error": str(e)}), 500
        
    return bp
# def create_performance_mutual_funds_bp(performance_mutual_funds_service: PerformanceMutualFundsService):
#     bp = Blueprint('performance-mutual-funds', __name__, url_prefix='/api/performance-mutual-funds')
#     logger = logging.getLogger(__name__)

#     @bp.route('/<fund_name>', methods=['GET'])
#     def get_performance_by_fund(fund_name: str):
#         try:
#             logger.info(f"Getting performance for fund: {fund_name}")
#             performance = performance_mutual_funds_service.get_performance_by_fund(fund_name)
#             return jsonify(performance), 200
#         except Exception as e:
#             logger.error(f"Error getting performance by fund: {str(e)}")
#             return jsonify({"error": str(e)}), 500

#     @bp.route('/<fund_name>/date/<date>', methods=['GET'])
#     def get_performance_by_fund_and_date(fund_name: str, date: str):
#         try:
#             logger.info(f"Getting performance for fund {fund_name} on date {date}")
#             date_obj = datetime.strptime(date, '%Y-%m-%d').date()
#             performance = performance_mutual_funds_service.get_performance_by_fund_and_date(fund_name, date_obj)
#             return jsonify(performance), 200
#         except ValueError:
#             return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
#         except Exception as e:
#             logger.error(f"Error getting performance by fund and date: {str(e)}")
#             return jsonify({"error": str(e)}), 500

#     return bp