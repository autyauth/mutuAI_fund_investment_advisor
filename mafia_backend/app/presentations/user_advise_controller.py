from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.auth_utils import user_access_required
from utils.auth_utils import admin_access_required
from services.advisor_service import AdvisorService
from services.exceptions import UserNotFoundException, ValidationError, InternalErrorException
from dto.user_advise_dto import UserAdviseDTO
from services.user_service import UserService

from datetime import datetime
import logging
from adapters.exceptions import *

def user_advise_bp(advise_service: AdvisorService, user_service: UserService):
    bp = Blueprint('user_advise', __name__, url_prefix='/api/user-advise')
    logger = logging.getLogger(__name__)

    @bp.route('/user/<username>', methods=['GET'])
    @jwt_required()
    @user_access_required
    def get_user_advise(username: str):
        try:
            user_service.get_user_by_username(username)
            user_advise = advise_service.analyze_and_advise_user_funds(username, datetime.now())
            return jsonify(user_advise), 200
        except UserNotFoundException as e:
            return jsonify({
                'status': 'error',
                **e.to_dict()
            }), 404

    return bp

    