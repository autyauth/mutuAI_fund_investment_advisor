from flask import Blueprint, jsonify
from services.notification_service import NotificationService

def create_notification_bp(notification_service: NotificationService):
    bp = Blueprint('notification', __name__, url_prefix='/api/notification')

    @bp.route('/user/<username>', methods=['GET'])
    def get_user_notifications(username: str):
        try:
            notifications = notification_service.get_notifications_by_username(username)
            return jsonify(notifications), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return bp