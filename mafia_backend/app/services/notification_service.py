from services.exceptions import BusinessLogicException
from adapters.repositories.notification_repository import NotificationRepository

class NotificationService:
    def __init__(self, notification_repository: NotificationRepository):
        self.notification_repository = notification_repository

    def get_notifications_by_username(self, username: str):
        notifications = self.notification_repository.get_notifications_by_username(username)
        if not notifications:
            return []
        return [self._notification_to_dto(n) for n in notifications]

    def _notification_to_dto(self, notification):
        return {
            'message': notification.message,
            'timestamp': notification.timestamp.isoformat(),
            'picture': notification.picture,
            'is_read': notification.is_read
        }