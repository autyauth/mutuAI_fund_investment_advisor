from flask import Blueprint, request, jsonify
from services.auth_service import AuthService
from datetime import datetime, date
from services.exceptions import BusinessLogicException
import logging

def create_auth_bp(auth_service: AuthService):
    bp = Blueprint('auth', __name__, url_prefix='/api/auth')
    logger = logging.getLogger(__name__)

    @bp.route('/register', methods=['POST'])
    def register():
        try:
            logger.info("Starting registration process")
            data = request.get_json()
            logger.debug(f"Received registration data: {data}")
            
            # Validate required fields
            required_fields = ['username', 'password', 'email', 'telephone_number', 'birthday']
            for field in required_fields:
                if not data.get(field):
                    logger.warning(f"Missing required field: {field}")
                    return jsonify({"error": f"Missing required field: {field}"}), 400

            try:
                birthday = datetime.strptime(data['birthday'], '%Y-%m-%d').date()
            except ValueError as e:
                logger.warning(f"Invalid birthday format: {e}")
                return jsonify({"error": "Invalid birthday format. Use YYYY-MM-DD"}), 400

            # Register user with detailed logging
            logger.info(f"Attempting to register user: {data['username']}")
            result = auth_service.register(
                username=data['username'],
                password=data['password'],
                email=data['email'],
                telephone_number=data['telephone_number'],
                birthday=birthday
            )
            
            logger.info(f"Successfully registered user: {data['username']}")
            return jsonify(result), 201

        except BusinessLogicException as e:
            logger.error(f"Business logic error during registration: {str(e)}")
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            logger.error(f"Unexpected error during registration: {str(e)}", exc_info=True)
            return jsonify({"error": str(e)}), 500

    @bp.route('/login', methods=['POST'])
    def login():
        try:
            data = request.get_json()
            logger.info(f"Login attempt for username: {data.get('username')}")
            
            if not data:
                return jsonify({"error": "No data provided"}), 400

            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return jsonify({"error": "Username and password required"}), 400

            result = auth_service.authenticate(username, password)
            logger.info(f"Login successful for username: {username}")
            return jsonify(result), 200

        except Exception as e:
            logger.error(f"Login failed: {str(e)}", exc_info=True)
            return jsonify({"error": str(e)}), 401

    return bp