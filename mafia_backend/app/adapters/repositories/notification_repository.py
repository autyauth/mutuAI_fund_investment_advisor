from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from adapters.database.mysql_database import MysqlDatabase
from adapters.models import NotificationModel
from adapters.repositories.interfaces.INotification_repository import INotificationRepository
from adapters.exceptions import *
import logging

class NotificationRepository(INotificationRepository):
    def __init__(self, database: MysqlDatabase):
        self.database = database
        self.logger = logging.getLogger(__name__)

    def get_notifications_by_username(self, username: str) -> list[NotificationModel]:
        session: Session = self.database.Session()
        try:
            notifications = (
                session.query(NotificationModel)
                .filter(NotificationModel.username == username)
                .order_by(NotificationModel.timestamp.desc())
                .all()
            )
            return notifications
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving notifications: {str(e)}")
            raise DatabaseException("Failed to retrieve notifications", e)
        finally:
            session.close()