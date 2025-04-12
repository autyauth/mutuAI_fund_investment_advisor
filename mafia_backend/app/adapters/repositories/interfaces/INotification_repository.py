from abc import ABC, abstractmethod
from adapters.models import NotificationModel

class INotificationRepository(ABC):
    @abstractmethod
    def get_notifications_by_username(self, username: str) -> list[NotificationModel]:
        pass