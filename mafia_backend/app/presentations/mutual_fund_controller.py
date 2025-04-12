from flask import Blueprint, jsonify
from services.mutual_fund_service import MutualFundService
from services.exceptions import BusinessLogicException
import logging

def create_mutual_fund_bp(mutual_fund_service: MutualFundService):
    bp = Blueprint('mutual_fund', __name__, url_prefix='/api/mutual-fund')
    logger = logging.getLogger(__name__)

    @bp.route('/', methods=['GET'])
    def get_all_mutual_funds():
        try:
            logger.info("Getting all mutual funds")
            mutual_funds = mutual_fund_service.get_all_mutual_funds()
            return jsonify(mutual_funds), 200
        except Exception as e:
            logger.error(f"Error getting mutual funds: {str(e)}")
            return jsonify({"error": str(e)}), 500

    @bp.route('/<fund_name>', methods=['GET'])
    def get_mutual_fund_by_name(fund_name: str):
        try:
            logger.info(f"Getting mutual fund: {fund_name}")
            mutual_fund = mutual_fund_service.get_mutual_fund_by_name(fund_name)
            return jsonify(mutual_fund), 200
        except BusinessLogicException as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            logger.error(f"Error getting mutual fund: {str(e)}")
            return jsonify({"error": str(e)}), 500

    return bp