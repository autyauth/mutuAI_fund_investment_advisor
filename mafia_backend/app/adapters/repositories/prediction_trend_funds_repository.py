from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import text
from adapters.models import PredictionTrendFundsModel
from adapters.exceptions import *
from datetime import date
import logging
from datetime import datetime

class PredictionTrendFundsRepository:
    def __init__(self, database):
        self.database = database
        self.logger = logging.getLogger(__name__)

    def get_prediction_trend_funds(self, fund_name: str, date: str) -> PredictionTrendFundsModel:
        session: Session = self.database.Session()
        try:
            prediction_trend_funds = (
                session.query(PredictionTrendFundsModel)
                .filter(
                    PredictionTrendFundsModel.fund_name == fund_name, 
                    PredictionTrendFundsModel.date == datetime.strptime(date, "%Y-%m-%d")
                )
                .first()
            )
            if prediction_trend_funds is None:
                raise RecordNotFoundException(f"Prediction trend funds not found for fund {fund_name} and date {date}")
            return prediction_trend_funds
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving notifications: {str(e)}")
            raise DatabaseException("Failed to retrieve prediction trend funds.", e) from e
        finally:
            session.close()

    def get_mutual_all_prediction_trend_funds(self, fund_name: str) -> list[PredictionTrendFundsModel]:
        session: Session = self.database.Session()
        try:
            prediction_trend_funds = (
                session.query(PredictionTrendFundsModel)
                .filter(PredictionTrendFundsModel.fund_name == fund_name)
                .all()
            )
            if prediction_trend_funds is None or len(prediction_trend_funds) == 0:
                raise RecordNotFoundException(f"Prediction trend funds not found for fund {fund_name} and date {date}")
            return prediction_trend_funds
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving prediction trend funds: {str(e)}")
            raise DatabaseException("Failed to retrieve prediction trend funds", e)
        finally:
            session.close()
            
    def get_prediction_trend_funds_lastest(self, fund_name: str) -> PredictionTrendFundsModel:
        session: Session = self.database.Session()
        try:
            prediction_trend_funds = (
                session.query(PredictionTrendFundsModel)
                .filter(
                    PredictionTrendFundsModel.fund_name == fund_name, 
                )
                .order_by(PredictionTrendFundsModel.date.desc())
                .first()
            )
            if prediction_trend_funds is None:
                raise RecordNotFoundException(f"Prediction trend funds not found for fund {fund_name} and date {date}")
            return prediction_trend_funds
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving notifications: {str(e)}")
            raise DatabaseException("Failed to retrieve prediction trend funds.", e) from e
        finally:
            session.close()
    
    def get_prediction_trend_funds_lastest_all(self) -> list[PredictionTrendFundsModel]:
        session: Session = self.database.Session()
        try:
            prediction_trend_funds = (
                session.query(PredictionTrendFundsModel)
                .from_statement(text(
                """SELECT * FROM prediction_trend_funds AS p
                WHERE date = (
                    SELECT MAX(date) 
                    FROM prediction_trend_funds AS sub
                    WHERE sub.fund_name = p.fund_name
                );"""))
                .all()
            )
            if prediction_trend_funds is None or len(prediction_trend_funds) == 0:
                return []
            return prediction_trend_funds
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving notifications: {str(e)}")
            raise DatabaseException("Failed to retrieve prediction trend funds.", e) from e
        finally:
            session.close()
            
    def get_prediction_trend_by_fund_name_and_date_range(self, fund_name: str, start_date: date, end_date: date) -> list[PredictionTrendFundsModel]:
        session: Session = self.database.Session()
        try:
            prediction_trend_funds = (
                session.query(PredictionTrendFundsModel)
                .filter(
                    PredictionTrendFundsModel.fund_name == fund_name,
                    PredictionTrendFundsModel.date >= start_date,
                    PredictionTrendFundsModel.date <= end_date
                )
                .all()
            )
            if prediction_trend_funds is None or len(prediction_trend_funds) == 0:
                raise RecordNotFoundException(f"Prediction trend funds not found for fund {fund_name}")
            return prediction_trend_funds
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving prediction trend funds: {str(e)}")
            raise DatabaseException("Failed to retrieve prediction trend funds", e)
        finally:
            session.close()

    def create_prediction_trend_funds(self, prediction_trend_funds: PredictionTrendFundsModel) -> None:
        session: Session = self.database.Session()
        try:
            session.add(prediction_trend_funds)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            if "duplicate" in str(e.orig).lower():
                self.logger.error(f"entry duplicate : {str(e)}")
                raise DuplicateEntryException(
                    f"Prediction trend funds already exists for fund {prediction_trend_funds.fund_name}", e
                ) from e
            raise DatabaseException("Integrity error occurred while creating prediction trend funds.", e) from e
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Database error while retrieving notifications: {str(e)}")
            raise DatabaseException("Failed to create prediction trend funds.", e) from e
        finally:
            session.close()
    
    def create_or_update_prediction_trend_funds(self, prediction_trend_funds: PredictionTrendFundsModel) -> None:
        session: Session = self.database.Session()
        try:
            session.merge(prediction_trend_funds)
            session.commit()
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving notifications: {str(e)}")
            session.rollback()
            raise DatabaseException("Failed to create or update prediction trend funds.", e) from e
        finally:
            session.close()
