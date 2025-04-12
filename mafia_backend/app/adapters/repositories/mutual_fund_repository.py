from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from adapters.database.mysql_database import MysqlDatabase
from adapters.models import MutualFundModel
from adapters.repositories.interfaces.IMutual_fund_repository import IMutualFundRepository
from adapters.exceptions import *
import logging

class MutualFundRepository(IMutualFundRepository):
    def __init__(self, database: MysqlDatabase):
        self.database = database
        self.logger = logging.getLogger(__name__)

    def get_all_mutual_funds(self) -> list[MutualFundModel]:
        session: Session = self.database.Session()
        try:
            mutual_funds = (
                session.query(MutualFundModel)
                .order_by(MutualFundModel.fund_name)
                .all()
            )
            return mutual_funds
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving mutual funds: {str(e)}")
            raise DatabaseException("Failed to retrieve mutual funds", e)
        finally:
            session.close()

    def get_mutual_fund_by_name(self, fund_name: str) -> MutualFundModel:
        session: Session = self.database.Session()
        try:
            mutual_fund = (
                session.query(MutualFundModel)
                .filter(MutualFundModel.fund_name == fund_name)
                .first()
            )
            return mutual_fund
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving mutual fund: {str(e)}")
            raise DatabaseException("Failed to retrieve mutual fund", e)
        finally:
            session.close()