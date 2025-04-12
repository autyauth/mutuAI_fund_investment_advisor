from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.auth_utils import user_access_required
from utils.auth_utils import admin_access_required
from services.prediction_trend_funds_service import PredictionTrendFundsService
from dto.prediction_trend_funds_dto import PredictionTrendFundsDTO
from adapters.models.prediction_trend_funds_model import PredictionTrendFundsModel

from datetime import datetime
import logging
from adapters.exceptions import *

def create_prediction_trend_funds_bp(prediction_trend_funds_service: PredictionTrendFundsService):
    bp = Blueprint('prediction_trend-funds', __name__, url_prefix='/api/prediction-trend-funds')
    logger = logging.getLogger(__name__)

    @bp.route('/', methods=['GET'])
    def get_prediction_trend_funds():
        try:
            fund_name = request.args.get("fund_name")
            date = request.args.get("date")
            if not fund_name or not date:
                raise ValueError("Missing required query parameter: fund_name or date")
            prediction_trend_funds = prediction_trend_funds_service.get_prediction_trend_funds(fund_name, date)
            return jsonify(prediction_trend_funds.to_dict()), 200
        except RecordNotFoundException as e:
            logging.error(f"Prediction trend funds not found: {str(e)}")
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            logging.error(f"Failed to retrieve prediction trend funds: {str(e)}")
            return jsonify({"error": str(e)}), 500

    @bp.route('/all', methods=['GET'])
    def get_mutual_all_prediction_trend_funds():
        try:
            fund_name = request.args.get("fund_name")
            if not fund_name:
                raise ValueError("Missing required query parameter: fund_name or date")
            prediction_trend_funds = prediction_trend_funds_service.get_mutual_all_prediction_trend_funds(fund_name)
            return jsonify([prediction_trend_fund.to_dict() for prediction_trend_fund in prediction_trend_funds]), 200
        except RecordNotFoundException as e:
            logging.error(f"Prediction trend funds not found: {str(e)}")
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            logging.error(f"Failed to retrieve mutual all prediction trend funds: {str(e)}")
            return jsonify({"error": str(e)}), 500
        
    @bp.route('/latest/<fund_name>', methods=['GET'])
    def get_prediction_trend_funds_lastest(fund_name: str):
        prediction_trend_funds = prediction_trend_funds_service.get_prediction_trend_funds_lastest(fund_name)
        return jsonify(prediction_trend_funds.to_dict()), 200
    
    @bp.route('/latest_all/', methods=['GET'])
    def get_prediction_trend_funds_lastest_all():
        prediction_trend_funds = prediction_trend_funds_service.get_prediction_trend_funds_lastest_all()
        return jsonify([prediction_trend_fund.to_dict() for prediction_trend_fund in prediction_trend_funds]), 200

    @bp.route('/range/<fund_name>', methods=['GET'])
    def get_prediction_trend_by_fund_name_and_date_range(fund_name: str):
        try:
            
            start_date = request.args.get("start_date")
            end_date = request.args.get("end_date")
            if not start_date or not end_date:
                raise ValueError("Missing required query parameter: start_date or end_date")
            username = get_jwt_identity()
            logger.info(f" {username} is request prediction trend funds for {fund_name} from {start_date} to {end_date}")
            prediction_trend_funds = prediction_trend_funds_service.get_prediction_trend_by_fund_name_and_date_range(fund_name, start_date, end_date)
            return jsonify([prediction_trend_fund.to_dict() for prediction_trend_fund in prediction_trend_funds]), 200
        except RecordNotFoundException as e:
            logging.error(f"Prediction trend funds not found: {str(e)}")
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            logging.error(f"Failed to retrieve prediction trend funds by fund name and date range: {str(e)}")
            return jsonify({"error": str(e)}), 500
    
    @bp.route('/add', methods=['POST'])
    @jwt_required()
    @admin_access_required
    def add_prediction_trend_funds():
        try:
            username = get_jwt_identity()
            logger.info(f" {username} is adding prediction trend funds")
            data = request.get_json()
            required_fields = ["fund_name", "date", "trend", "up_trend_prob", "down_trend_prob", "reason", "indicator"]
            for field in required_fields:
                if field not in data:
                    raise KeyError(f"Missing required field: {field}")
            try:
                parsed_date = datetime.strptime(data["date"], "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Invalid date format, expected YYYY-MM-DD")
            pred_dto = PredictionTrendFundsDTO(
                fund_name=data["fund_name"],
                date=parsed_date,
                trend=data["trend"],
                up_trend_prob=data["up_trend_prob"],
                down_trend_prob=data["down_trend_prob"],
                reason=data["reason"],
                indicator=data["indicator"]
            )
            
            prediction_trend_funds = prediction_trend_funds_service.add_prediction_trend_funds(pred_dto)
            return jsonify(prediction_trend_funds.to_dict()), 201
        except Exception as e:
            logging.error(f"Failed to add prediction trend funds: {str(e)}")
            return jsonify({"error": str(e)}), 500
        except ValueError as e:
            logging.error(f"Invalid value: {str(e)}")
            return jsonify({"error": str(e)}), 400
        except KeyError as e:
            logging.error(f"Missing required field: {str(e)}")
            return jsonify({"error": str(e)}), 400

    return bp

    