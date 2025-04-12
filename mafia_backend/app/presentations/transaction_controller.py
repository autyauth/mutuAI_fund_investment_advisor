from flask import Blueprint, request, jsonify
from dto.transaction_dto import TransactionDTO, TransactionType
from dto.fund_type_enum import FundType
from services.transaction_service import TransactionService
from datetime import datetime
from services.exceptions import BusinessLogicException
import logging
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.auth_utils import user_access_required

def create_transaction_bp(transaction_service: TransactionService):
    bp = Blueprint('transaction', __name__, url_prefix='/api/transaction')
    logger = logging.getLogger(__name__)

    @bp.route('/user/<username>', methods=['GET'])
    @jwt_required()
    @user_access_required
    def get_user_transactions(username: str):
        try:
            logger.info(f"Getting transactions for user: {username}")
            transactions = transaction_service.get_transactions_by_username(username)
            return jsonify(transactions), 200
        except BusinessLogicException as e:
            logger.error(f"Business logic error: {str(e)}")
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error(f"Unexpected error in get_user_transactions: {str(e)}")
            return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

    @bp.route('/buy', methods=['POST'])
    @jwt_required()
    def buy_fund():
        try:
            current_user = get_jwt_identity()  # Get user from JWT
            data = request.get_json()
            logger.info(f"Received buy request with data: {data}")  # Added logging
            keywords = ["SSF", "RMF", "THAIESG"]
            fund_type_tmp = ""
            for keyword in keywords:
                if keyword in data['fund_name'].upper():
                    fund_type_tmp = keyword
                    break
            transaction_dto = TransactionDTO(
                username=current_user,  # Use JWT user instead of request data
                fund_name=data['fund_name'],
                transaction_type=TransactionType.BUY,
                transaction_date=datetime.strptime(data['transaction_date'], '%Y-%m-%d').date(),
                units_processed=float(data['units_processed']),
                amount_processed=float(data['amount_processed']),
                processed_nav=float(data['processed_nav']),
                fund_type=FundType[data.get('fund_type', fund_type_tmp)]  # Get fund type from request
            )

            logger.info(f"Processing buy transaction for user: {current_user}")
            transaction_service.process_buy_transaction(transaction_dto)
            return jsonify({"message": "Buy transaction processed successfully"}), 200

        except KeyError as e:
            logger.error(f"Missing required field: {str(e)}")
            return jsonify({"error": f"Missing required field: {str(e)}"}), 400
        except ValueError as e:
            logger.error(f"Invalid value: {str(e)}")
            return jsonify({"error": f"Invalid value: {str(e)}"}), 400
        except BusinessLogicException as e:
            logger.error(f"Business logic error: {str(e)}")
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error(f"Unexpected error in buy_fund: {str(e)}")
            return jsonify({"error": "An unexpected error occurred"}), 500

    @bp.route('/sell', methods=['POST'])
    @jwt_required()
    def sell_fund():
        try:
            data = request.get_json()
            current_user = get_jwt_identity()  # Get user from JWT
            if current_user != data['username']:
                return jsonify({"error": "Access denied"}), 403
            transaction_dto = TransactionDTO(
                username=data['username'],
                fund_name=data['fund_name'],
                transaction_type=TransactionType.SELL,
                transaction_date=datetime.strptime(data['transaction_date'], '%Y-%m-%d').date(),
                units_processed=float(data['units_processed']),
                amount_processed=float(data['amount_processed']),
                processed_nav=float(data['processed_nav']),
                fund_type=FundType[data.get('fund_type', 'RMF')]
            )

            transaction_service.process_sell_transaction(transaction_dto)
            return jsonify({"message": "Sell transaction processed successfully"}), 200

        except KeyError as e:
            return jsonify({"error": f"Missing required field: {str(e)}"}), 400
        except ValueError as e:
            return jsonify({"error": f"Invalid value: {str(e)}"}), 400
        except BusinessLogicException as e:
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return bp