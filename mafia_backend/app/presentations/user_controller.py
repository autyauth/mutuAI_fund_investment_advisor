from flask import Blueprint, jsonify, request
from services.user_service import UserService
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.auth_utils import user_access_required
from services.exceptions import UserNotFoundException, ValidationError, InternalErrorException

def create_user_bp(user_service: UserService):
    bp = Blueprint('user', __name__, url_prefix='/api/user')

    @bp.route('/<username>', methods=['GET'])
    @jwt_required()
    @user_access_required
    def get_user(username: str):
        try:
            user = user_service.get_user_by_username(username)
            if not user:
                return jsonify({"error": "User not found"}), 404
            return jsonify(user), 200
        except UserNotFoundException as e:
            return jsonify({
                'status': 'error',
                **e.to_dict()
            }), 404
        except Exception as e:
            return jsonify({
                'status': 'error',
                **InternalErrorException(error=e).to_dict()
            }), 500

    @bp.route('/<username>', methods=['POST'])
    @jwt_required()
    @user_access_required
    def update_user_by_username(username: str):
        try:
            current_user = get_jwt_identity()
            # Optional: Add permission check here if needed
            data = request.get_json()
            
            update_data = {}
            if 'email' in data:
                update_data['email'] = data['email']
            if 'telephone_number' in data:
                update_data['telephone_number'] = data['telephone_number']
            if 'birthday' in data:
                update_data['birthday'] = data['birthday']
            if 'job' in data:
                update_data['job'] = data['job']
            
            if not update_data:
                return jsonify({
                    'status': 'error',
                    'message': 'No valid fields to update'
                }), 400
                
            user = user_service.update_user_info(username, update_data)
            
            return jsonify({
                'status': 'success',
                'message': 'User information updated successfully',
                'data': {
                    'username': user.username,
                    'email': user.email,
                    'telephone_number': user.telephone_number,
                    'birthday': user.birthday.isoformat() if user.birthday else None,
                    'job': user.job
                }
            }), 200
            
        except ValidationError as e:
            return jsonify({
                'status': 'error',
                **e.to_dict()
            }), 400
        except UserNotFoundException as e:
            return jsonify({
                'status': 'error',
                **e.to_dict()
            }), 404
        except Exception as e:
            return jsonify({
                'status': 'error',
                **InternalErrorException(error=e).to_dict()
            }), 500
    
    @bp.route('/<username>/risk-level/', methods=['POST'])
    @jwt_required()
    @user_access_required
    def update_user_risk_level(username: str):
        try:
            current_user = get_jwt_identity()
            # Optional: Add permission check here if needed
            data = request.get_json()
            risk_level = data.get('risk_level')
            if risk_level is None:
                return jsonify({
                    'status': 'error',
                    'message': 'Risk level is required'
                }), 400
            
            user = user_service.update_user_risk_level(username, risk_level)
            
            return jsonify({
                'status': 'success',
                'message': 'User risk level updated successfully',
                'data': {
                    'username': user.username,
                    'risk_level': user.risk_level
                }
            }), 200
            
        except ValidationError as e:
            return jsonify({
                'status': 'error',
                **e.to_dict()
            }), 400
        except UserNotFoundException as e:
            return jsonify({
                'status': 'error',
                **e.to_dict()
            }), 404
        except Exception as e:
            return jsonify({
                'status': 'error',
                **InternalErrorException(error=e).to_dict()
            }), 500
    

    return bp