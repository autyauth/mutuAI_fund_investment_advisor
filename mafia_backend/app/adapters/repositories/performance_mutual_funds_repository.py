from adapters.models.performance_mutual_funds_model import PerformanceMutualFundsModel
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import text
from adapters.exceptions import *
from datetime import date
import logging
from datetime import datetime

class PerformanceMutualFundsRepository:
    def __init__(self, database):
        self.database = database
        self.logger = logging.getLogger(__name__)

    def get_performance_mutual_funds(self, fund_name: str, date: str) -> PerformanceMutualFundsModel:
        session: Session = self.database.Session()
        try:
            performance_mutual_funds = (
                session.query(PerformanceMutualFundsModel)
                .filter(
                    PerformanceMutualFundsModel.fund_name == fund_name, 
                    PerformanceMutualFundsModel.date == datetime.strptime(date, "%Y-%m-%d")
                )
                .first()
            )
            if performance_mutual_funds is None:
                raise RecordNotFoundException(f"Performance mutual funds not found for fund {fund_name} and date {date}")
            return performance_mutual_funds
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving notifications: {str(e)}")
            raise DatabaseException("Failed to retrieve performance mutual funds.", e) from e
        finally:
            session.close()

    def get_mutual_all_performance_mutual_funds(self, fund_name: str) -> list[PerformanceMutualFundsModel]:
        session: Session = self.database.Session()
        try:
            performance_mutual_funds = (
                session.query(PerformanceMutualFundsModel)
                .filter(PerformanceMutualFundsModel.fund_name == fund_name)
                .all()
            )
            if performance_mutual_funds is None or len(performance_mutual_funds) == 0:
                raise RecordNotFoundException(f"Performance mutual funds not found for fund {fund_name} and date {date}")
            return performance_mutual_funds
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving performance mutual funds: {str(e)}")
            raise DatabaseException("Failed to retrieve performance mutual funds", e)
        finally:
            session.close()
            
    def get_performance_mutual_funds_lastest(self, fund_name: str) -> PerformanceMutualFundsModel:
        session: Session = self.database.Session()
        try:
            performance_mutual_funds = (
                session.query(PerformanceMutualFundsModel)
                .filter(
                    PerformanceMutualFundsModel.fund_name == fund_name, 
                )
                .order_by(PerformanceMutualFundsModel.date.desc())
                .first()
            )
            if performance_mutual_funds is None:
                raise RecordNotFoundException(f"Performance mutual funds not found for fund {fund_name}")
            return performance_mutual_funds
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving notifications: {str(e)}")
            raise DatabaseException("Failed to retrieve performance mutual funds.", e) from e
        finally:
            session.close()
    
    def create_performance_mutual_funds(self, performance_mutual_funds: PerformanceMutualFundsModel):
        session: Session = self.database.Session()
        try:
            session.add(performance_mutual_funds)
            session.commit()
        except IntegrityError as e:
            self.logger.error(f"Database error while creating performance mutual funds: {str(e)}")
            raise DatabaseException("Failed to create performance mutual funds.", e) from e
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while creating performance mutual funds: {str(e)}")
            raise DatabaseException("Failed to create performance mutual funds.", e) from e
        finally:
            session.close()
            
    def create_or_update_performance_mutual_funds(self, performance_mutual_funds: PerformanceMutualFundsModel):
        session: Session = self.database.Session()
        try:
            session.merge(performance_mutual_funds)
            session.commit()
        except IntegrityError as e:
            self.logger.error(f"Database error while creating performance mutual funds: {str(e)}")
            raise DatabaseException("Failed to create performance mutual funds.", e) from e
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while creating performance mutual funds: {str(e)}")
            raise DatabaseException("Failed to create performance mutual funds.", e) from e
        finally:
            session.close()