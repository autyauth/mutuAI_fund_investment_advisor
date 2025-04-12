from adapters.database.mysql_database import MysqlDatabase
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import text
from adapters.models import DeductionModel
from adapters.exceptions import *
import logging

class DeductionRepository:
    def __init__(self, database: MysqlDatabase):
        self.database = database
        self.logger = logging.getLogger(__name__)

    def get_deduction(self, username: str, year: int):
        session = self.database.Session()
        try:
            deduction = session.query(DeductionModel).filter_by(username=username, year=year).first()
            return deduction
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while getting deduction: {str(e)}")
            raise DatabaseException("Failed to get deduction", e)
        finally:
            session.close()
    
    def get_sum_rmf_ssf_thaiesg_deduction(self, username: str, year: int):
        session = self.database.Session()
        try:
            deduction = (
                session.query(DeductionModel.rmf, DeductionModel.ssf, DeductionModel.thai_esg)
                .filter_by(username=username, year=year)
                .first()
            )
            if deduction is None:
                return 0
            sum_deduction = deduction.rmf if deduction.rmf is not None else 0
            sum_deduction += deduction.ssf if deduction.ssf is not None else 0
            sum_deduction += deduction.thai_esg if deduction.thai_esg is not None else 0
            return sum_deduction
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while getting deduction: {str(e)}")
            raise DatabaseException("Failed to get deduction", e)
        finally:
            session.close()