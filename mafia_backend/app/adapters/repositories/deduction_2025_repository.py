from adapters.database.mysql_database import MysqlDatabase
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import text
from adapters.models import Deduction2025Model
from adapters.exceptions import *
import logging

class Deduction2025Repository:
    def __init__(self, database: MysqlDatabase):
        self.database = database
        self.logger = logging.getLogger(__name__)

    def save_deduction(self, deduction: Deduction2025Model):
        session = self.database.Session()
        try:
            session.merge(deduction)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Database error while saving deduction: {str(e)}")
            raise DatabaseException("Failed to save deduction", e)
        finally:
            session.close()
    def get_deduction(self, username: str, year: int):
        session = self.database.Session()
        try:
            deduction = session.query(Deduction2025Model).filter_by(username=username, year=year).first()
            return deduction
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while getting deduction: {str(e)}")
            raise DatabaseException("Failed to get deduction", e)
        finally:
            session.close()
    
    def get_sum_rmf_thaiesg_deduction(self, username: str, year: int):
        session = self.database.Session()
        try:
            deduction = (
                session.query(Deduction2025Model.rmf_fund, Deduction2025Model.thai_esg)
                .filter_by(username=username, year=year)
                .first()
            )
            if deduction is None:
                return 0
            sum_deduction = deduction.rmf_fund if deduction.rmf_fund is not None else 0
            sum_deduction += deduction.thai_esg if deduction.thai_esg is not None else 0
            return sum_deduction
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while getting deduction: {str(e)}")
            raise DatabaseException("Failed to get deduction", e)
        finally:
            session.close()