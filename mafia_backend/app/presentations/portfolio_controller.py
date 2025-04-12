from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from utils.auth_utils import user_access_required
from services.portfolio_service import PortfolioService
import logging

def create_portfolio_bp(portfolio_service: PortfolioService):
    bp = Blueprint('portfolio', __name__, url_prefix='/api/portfolio')
    logger = logging.getLogger(__name__)

    @bp.route('/user/<username>', methods=['GET'])
    @jwt_required()
    @user_access_required
    def get_user_portfolio(username: str):
        try:
            logger.info(f"Getting all portfolio for user {username}")
            portfolio = portfolio_service.get_all_portfolio_by_username(username)
            return jsonify(portfolio), 200
        except Exception as e:
            logger.error(f"Error getting portfolio: {str(e)}")
            return jsonify({"error": str(e)}), 500

    @bp.route('/user/<username>/year/<int:year>', methods=['GET'])
    @jwt_required()
    @user_access_required
    def get_user_portfolio_by_year(username: str, year: int):
        try:
            logger.info(f"Getting portfolio for user {username} year {year}")
            portfolio = portfolio_service.get_portfolio_by_year(username, year)
            return jsonify(portfolio), 200
        except Exception as e:
            logger.error(f"Error getting portfolio: {str(e)}")
            return jsonify({"error": str(e)}), 500

    return bp  # This return statement is critical