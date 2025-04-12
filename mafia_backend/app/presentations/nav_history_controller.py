from flask import Blueprint, request, jsonify
from services.nav_history_service import NavHistoryService
from datetime import datetime
from services.exceptions import BusinessLogicException
import logging
from dto.nav_history_dto import NavHistoryDTO
from adapters.exceptions import RecordNotFoundException
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.auth_utils import admin_access_required
from services.performance_mutual_funds_service import PerformanceMutualFundsService
from services.portfolio_service import PortfolioService

def create_nav_history_bp(nav_history_service: NavHistoryService, performance_mutual_funds_service: PerformanceMutualFundsService, portfolio_service: PortfolioService):
    bp = Blueprint('nav_history', __name__, url_prefix='/api/nav-history')
    logger = logging.getLogger(__name__)

    @bp.route('/latest', methods=['GET'])
    def get_latest_nav_all_funds():
        try:
            logger.info("Getting latest NAV for all funds")
            nav_histories = nav_history_service.get_nav_history_lastest_date_all_fund()
            return jsonify(nav_histories), 200
        except RecordNotFoundException as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            logger.error(f"Error getting latest NAV: {str(e)}")
            return jsonify({"error": str(e)}), 500

    @bp.route('/fund/<fund_name>', methods=['GET'])
    def get_nav_by_fund(fund_name: str):
        try:
            logger.info(f"Getting NAV history for fund: {fund_name}")
            nav_histories = nav_history_service.get_all_nav_history_by_fund_name(fund_name)
            return jsonify(nav_histories), 200
        except RecordNotFoundException as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            logger.error(f"Error getting NAV by fund: {str(e)}")
            return jsonify({"error": str(e)}), 500

    @bp.route('/date/<date>', methods=['GET'])
    def get_nav_by_date(date: str):
        try:
            logger.info(f"Getting NAV history for date: {date}")
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            nav_histories = nav_history_service.get_nav_history_by_date(date_obj)
            return jsonify(nav_histories), 200
        
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
        except RecordNotFoundException as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            logger.error(f"Error getting NAV by date: {str(e)}")
            return jsonify({"error": str(e)}), 500

    @bp.route('/fund/<fund_name>/date/<date>', methods=['GET'])
    def get_nav_by_fund_and_date(fund_name: str, date: str):
        try:
            logger.info(f"Getting NAV history for fund {fund_name} on date {date}")
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            nav_history = nav_history_service.get_nav_history_by_fund_name_and_date(fund_name, date_obj)
            return jsonify(nav_history), 200
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
        except RecordNotFoundException as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            logger.error(f"Error getting NAV by fund and date: {str(e)}")
            return jsonify({"error": str(e)}), 500

    @bp.route('/all', methods=['GET'])
    def get_all_nav_history():
        try:
            logger.info("Getting all NAV history")
            nav_histories = nav_history_service.get_all_nav_history()
            return jsonify(nav_histories), 200
        except RecordNotFoundException as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            logger.error(f"Error getting all NAV history: {str(e)}")
            return jsonify({"error": str(e)}), 500
        
    @bp.route('/range/<fund_name>', methods=['GET'])
    def get_range_nav_history(fund_name: str):
        try:
            logger.info("Getting range NAV history")
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            if not start_date or not end_date:
                raise ValueError("Missing required query parameter: start_date or end_date")
            logger.info(f"Getting NAV history from {start_date} to {end_date}")
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
            nav_histories = nav_history_service.get_nav_history_by_date_range(fund_name, start_date_obj, end_date_obj)
            return jsonify(nav_histories), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except RecordNotFoundException as e:
            return jsonify({"error": str(e)}), 404
        except BusinessLogicException as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error(f"Error getting range NAV history: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @bp.route('/fund/<fund_name>/window/<window>', methods=['GET'])
    def get_nav_history_by_fund_and_window(fund_name: str, window: int):
        try:
            logger.info(f"Getting NAV history for fund: {fund_name} with window: {window}")
            if (str(window).isnumeric() == False):
                raise ValueError("Window size must be a number")
            if (int(window) < 1):
                raise ValueError("Invalid window size")
            
            nav_histories = nav_history_service.get_nav_history_by_fund_name_and_window(fund_name, window)
            return jsonify(nav_histories), 200
        except RecordNotFoundException as e:
            return jsonify({"error": str(e)}), 404
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error(f"Error getting NAV by fund and window: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @bp.route('/add', methods=['POST'])
    @jwt_required()
    @admin_access_required
    def add_nav_history():
        try:
            logger.info("Adding new NAV history")
            nav_history = request.get_json()
            
            nav_history_fileds = ['fund_name', 'date', 'nav', 'fund_type', 'selling_price', 'redemption_price', 'total_net_assets', 'change']
            if not all(field in nav_history for field in nav_history_fileds):
                raise KeyError("Missing required field")
            nav_history['date'] = datetime.strptime(nav_history['date'], '%Y-%m-%d').date()
            nav_history_copy = nav_history.copy()
            fund_name = nav_history_copy['fund_name']
            nav = float(nav_history_copy['nav'])
            nav_history_model = NavHistoryDTO(**nav_history).to_model()
            nav_history_added = nav_history_service.add_nav_history(nav_history_model)

            performance_metrix = performance_mutual_funds_service.create_performance_mutual_funds(nav_history_copy['fund_name'], nav_history_copy['date'])
            
            portfolio_service.update_gain_loss_and_nav_present(fund_name, nav)
            
            nav_history_added_dict = nav_history_added.to_dict()
            nav_history_added_dict['date'] = nav_history_added_dict['date'].strftime('%Y-%m-%d')
            nav_history_added_dict.update(performance_metrix)
            return jsonify(nav_history_added_dict), 201
        except BusinessLogicException as e:
            logger.error(f"Error adding NAV history: {str(e)}")
            return jsonify({"error": str(e)}), 400
        except KeyError as e:
            logger.error(f"Missing required field: {str(e)}")
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error(f"Error adding NAV history: {str(e)}")
            return jsonify({"error": str(e)}), 500
    return bp