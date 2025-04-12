from flask import Blueprint, jsonify
from services.goal_service import GoalService
from flask_jwt_extended import jwt_required
from utils.auth_utils import user_access_required
from flask import request

def create_goal_bp(goal_service: GoalService):
    bp = Blueprint('goal', __name__, url_prefix='/api/goal')

    @bp.route('/user/<username>', methods=['GET'])
    @jwt_required()
    @user_access_required
    def get_user_goals(username: str):
        try:
            goals = goal_service.get_goals_by_username(username)
            return jsonify(goals), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    @bp.route('/user/<username>/year/<year>', methods=['GET'])
    @jwt_required()
    @user_access_required
    def get_user_goals_year(username: str, year: int):
        try:
            goals = goal_service.get_goal_by_username_and_year(username, year)
            return jsonify(goals), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    @bp.route('/rate-std/user/<username>', methods=['POST'])
    @jwt_required()
    @user_access_required
    def update_user_goal(username: str):
        try:
            data = request.get_json()
            data['username'] = username

            if 'rate_fund' in data:
                rate_fund = data['rate_fund']
                if not isinstance(rate_fund, (int, float)) or rate_fund < 0:
                    return jsonify({"error": "Invalid rate_fund value"}), 400
                goal_service.update_rate(data)

            if 'std_fund' in data:
                std_fund = data['std_fund']
                if not isinstance(std_fund, (int, float)) or std_fund < 0:
                    return jsonify({"error": "Invalid std_fund value"}), 400
                goal_service.update_std(data)

            return jsonify({"message": "Goal updated successfully"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return bp