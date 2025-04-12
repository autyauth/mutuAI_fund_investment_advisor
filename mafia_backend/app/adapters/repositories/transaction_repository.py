from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import text
from adapters.database.mysql_database import MysqlDatabase
from adapters.models import TransactionModel
from adapters.repositories.interfaces.ITransaction_repository import ITransactionRepository
from adapters.exceptions import *
from datetime import date
import logging
import pendulum

class TransactionRepository(ITransactionRepository):
    def __init__(self, database: MysqlDatabase):
        self.database = database
        self.logger = logging.getLogger(__name__)

    def create_transaction(self, username: str, fund_name: str, transaction_type: int,
                        transaction_date: date, units_processed: float, amount_processed: float,
                        processed_nav: float, gain_loss_percent: float, gain_loss_value: float) -> int:
        session: Session = self.database.Session()
        try:
            self.logger.info(f"Creating transaction: username={username}, fund={fund_name}, type={transaction_type}")
            
            # Debug log all parameters
            self.logger.info(f"Transaction parameters: "
                            f"date={transaction_date}, "
                            f"units={units_processed}, "
                            f"amount={amount_processed}, "
                            f"nav={processed_nav}, "
                            f"gain_loss_percent={gain_loss_percent}, "
                            f"gain_loss_value={gain_loss_value}")
            
            # Check if user exists
            user_exists = session.execute(
                text("SELECT 1 FROM users WHERE username = :username"),
                {"username": username}
            ).scalar() is not None

            if not user_exists:
                raise RecordNotFoundException(f"User {username} not found")

            # Check if fund exists
            fund_exists = session.execute(
                text("SELECT 1 FROM mutual_funds WHERE fund_name = :fund_name"),
                {"fund_name": fund_name}
            ).scalar() is not None

            if not fund_exists:
                raise RecordNotFoundException(f"Fund {fund_name} not found")
            
            result = session.execute(
                text("""
                    INSERT INTO transactions (
                        username, fund_name, transaction_type, transaction_date,
                        units_processed, amount_processed, processed_nav,
                        gain_loss_percent, gain_loss_value
                    ) VALUES (
                        :username, :fund_name, :transaction_type, :transaction_date,
                        :units_processed, :amount_processed, :processed_nav,
                        :gain_loss_percent, :gain_loss_value
                    )
                """),
                {
                    "username": username,
                    "fund_name": fund_name,
                    "transaction_type": transaction_type,
                    "transaction_date": transaction_date,
                    "units_processed": units_processed,
                    "amount_processed": amount_processed,
                    "processed_nav": processed_nav,
                    "gain_loss_percent": gain_loss_percent,
                    "gain_loss_value": gain_loss_value
                }
            )
            session.commit()
            self.logger.info("Transaction created successfully")
            return result.lastrowid
            
        except RecordNotFoundException as e:
            session.rollback()
            self.logger.error(f"Record not found: {str(e)}")
            raise
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Database error while creating transaction: {str(e)}")
            raise DatabaseException(f"Failed to create transaction record: {str(e)}")
        except Exception as e:
            session.rollback()
            self.logger.error(f"Unexpected error while creating transaction: {str(e)}")
            raise
        finally:
            session.close()

    def get_transactions_by_username(self, username: str) -> list[TransactionModel]:
        session: Session = self.database.Session()
        try:
            transactions = (
                session.query(TransactionModel)
                .filter(TransactionModel.username == username)
                .order_by(TransactionModel.transaction_date.desc())
                .all()
            )
            return transactions
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving transactions: {str(e)}")
            raise DatabaseException("Failed to retrieve transactions", e)
        finally:
            session.close()

    def get_transaction_by_id(self, transaction_id: int):
        session: Session = self.database.Session()
        try:
            result = session.execute(
                text("SELECT * FROM transactions WHERE transaction_id = :transaction_id"),
                {"transaction_id": transaction_id}
            ).fetchone()
            return result
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving transaction: {str(e)}")
            raise DatabaseException("Failed to retrieve transaction")
        finally:
            session.close()
    def get_transaction_by_username_current_month(self, username: str) -> list[TransactionModel]:
        local_tz = pendulum.timezone("Asia/Bangkok")
        start_of_month = pendulum.now(local_tz).start_of('month')
        end_of_month = pendulum.now(local_tz).end_of('month')
        session: Session = self.database.Session()
        try:
            transactions = (
                session.query(TransactionModel)
                .filter(TransactionModel.username == username)
                .filter(TransactionModel.transaction_date >= start_of_month)
                .filter(TransactionModel.transaction_date <= end_of_month)
                .all()
            )
            return transactions
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving transactions: {str(e)}")
            raise DatabaseException("Failed to retrieve transactions", e)
        finally:
            session.close()
        