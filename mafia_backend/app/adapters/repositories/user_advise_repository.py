from sqlalchemy.exc import SQLAlchemyError, DatabaseError
from sqlalchemy.orm import Session
from adapters.database.mysql_database import MysqlDatabase
from adapters.models.user_advise_model import UserAdviseModel
from adapters.exceptions import *
import logging

class UserAdviseRepository:
    def __init__(self, database: MysqlDatabase):
        self.database = database
        self.logger = logging.getLogger(__name__)
        
    def get_funds_by_username_and_year(self, username: str, year: int) -> list[UserAdviseModel]:
        session: Session = self.database.get_session()
        try:
            user_advise = session.query(UserAdviseModel.fund_name).filter(UserAdviseModel.username == username, UserAdviseModel.year == year).all()
            return user_advise
        except SQLAlchemyError as e:
            self.logger.error(f"Error: {e}")
            raise DatabaseError("Error while getting funds by username and year")
        finally:
            session.close()
    
    def create_user_advise(self, user_advise: UserAdviseModel) -> None:
        session: Session = self.database.get_session()
        try:
            session.add(user_advise)
            session.commit()
        except SQLAlchemyError as e:
            self.logger.error(f"Error: {e}")
            raise DatabaseError("Error while creating user advise")
        finally:
            session.close()

    