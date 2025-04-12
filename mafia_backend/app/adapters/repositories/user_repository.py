from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from adapters.database.mysql_database import MysqlDatabase
from adapters.models import UserModel
from adapters.repositories.interfaces.IUser_repository import IUserRepository
from adapters.exceptions import *
import logging
from services.exceptions import BusinessLogicException, NotFoundException
class UserRepository(IUserRepository):
    def __init__(self, database: MysqlDatabase):
        self.database = database
        self.logger = logging.getLogger(__name__)

    def get_user(self, username: str) -> UserModel:
        session: Session = self.database.Session()
        try:
            user = session.query(UserModel).filter(UserModel.username == username).first()
            return user
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving user: {str(e)}")
            raise DatabaseException("Failed to retrieve user", e)
        finally:
            session.close()

    def create_user(self, user_data: dict) -> None:
        session: Session = self.database.Session()
        try:
            new_user = UserModel(
                username=user_data['username'],
                password=user_data['password'],
                email=user_data['email'],
                telephone_number=user_data['telephone_number'],
                birthday=user_data['birthday'],
                risk_level=user_data['risk_level'],
                salary=user_data['salary']
            )
            session.add(new_user)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Database error while creating user: {str(e)}")
            raise DatabaseException("Failed to create user", e)
        finally:
            session.close()


    def get_by_username(self, username: str) -> UserModel:
        """Get user by username for authentication"""
        return self.get_user(username)

    def update(self, user_data: dict, username: str) -> UserModel:
        session: Session = self.database.Session()
        try:
            user = session.query(UserModel).filter(UserModel.username == username).first()
            if not user:
                raise NotFoundException(f"User {username} not found")
            user_copy = UserModel(
                username=user.username,
                email=user.email,
                telephone_number=user.telephone_number,
                birthday=user.birthday,
                risk_level=user.risk_level,
                salary=user.salary,
                job=user.job
            )
            for key, value in user_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)

            session.commit()
            return user_copy
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Database error while updating user: {str(e)}")
            raise DatabaseException("Failed to update user", e)
        finally:
            session.close()
            
    def update_risk_level(self, username: str, risk_level: int) -> UserModel:
        """Update user risk level"""
        if risk_level < 1 or risk_level > 5:
            raise BusinessLogicException("Risk level must be between 1 and 5")
        
        user = self.get_user(username)
        if not user:
            raise NotFoundException(f"User {username} not found")
        
        return self.update({'risk_level': risk_level}, username)
    
    def get_all_users(self) -> list:
        session: Session = self.database.Session()
        try:
            users = session.query(UserModel).all()
            return users
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving all users: {str(e)}")
            raise DatabaseException("Failed to retrieve all users", e)
        finally:
            session.close()