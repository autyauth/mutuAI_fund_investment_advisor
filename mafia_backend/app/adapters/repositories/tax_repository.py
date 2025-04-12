from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from adapters.database.mysql_database import MysqlDatabase
from adapters.models.tax_model import TaxModel
from adapters.exceptions import *
import logging

class TaxRepository:
    def __init__(self, database: MysqlDatabase):
        self.database = database
        self.logger = logging.getLogger(__name__)
    
    def get_tax_by_username(self, username: str) -> List[TaxModel]:
        """Get all tax records for a user"""
        session: Session = self.database.Session()
        try:
            self.logger.info(f"Fetching tax records by username: {username}")
            result = session.query(TaxModel).filter(TaxModel.username == username).all()
            self.logger.info(f"Tax records fetched successfully")
            return result
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while fetching tax: {str(e)}")
            raise DatabaseException("Failed to fetch tax record.", e) from e
        except Exception as e:
            self.logger.error(f"Unexpected error while fetching tax: {str(e)}")
            raise
        finally:
            session.close()
    
    def get_tax_by_username_year(self, username: str, year: int) -> Optional[TaxModel]:
        """Get specific tax record for a user and year"""
        session: Session = self.database.Session()
        try:
            self.logger.info(f"Fetching tax record by username and year: {username}, {year}")
            result = session.query(TaxModel).filter(
                TaxModel.username == username,
                TaxModel.year == year
            ).first()
            self.logger.info(f"Tax record fetched successfully")
            return result
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while fetching tax: {str(e)}")
            raise DatabaseException("Failed to fetch tax record.", e) from e
        except Exception as e:
            self.logger.error(f"Unexpected error while fetching tax: {str(e)}")
            raise
        finally:
            session.close()

    def save_tax(self, tax_data: dict) -> None:
        """
        Save or update tax record
        tax_data should contain: username, year, and users_tax
        """
        session: Session = self.database.Session()
        try:
            username = tax_data.get('username')
            year = tax_data.get('year')
            tax_amount = tax_data.get('users_tax')
            
            self.logger.info(f"Saving tax record: username={username}, year={year}, amount={tax_amount}")
            
            # Check if user exists
            user_exists = session.execute(
                text("SELECT 1 FROM users WHERE username = :username"),
                {"username": username}
            ).scalar() is not None

            if not user_exists:
                raise RecordNotFoundException(f"User {username} not found")

            # Save or update tax record
            tax_record = session.query(TaxModel).filter(
                TaxModel.username == username,
                TaxModel.year == year
            ).first()

            if tax_record:
                tax_record.users_tax = tax_amount
            else:
                tax_record = TaxModel(
                    username=username,
                    year=year,
                    users_tax=tax_amount
                )
                session.add(tax_record)

            session.commit()
            self.logger.info("Tax record saved successfully")
            
        except RecordNotFoundException as e:
            session.rollback()
            self.logger.error(f"User not found error: {str(e)}")
            raise
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Database error while saving tax: {str(e)}")
            raise DatabaseException("Failed to save tax record.", e) from e
        except Exception as e:
            session.rollback()
            self.logger.error(f"Unexpected error while saving tax: {str(e)}")
            raise
        finally:
            session.close()

    def delete_tax(self, username: str, year: int) -> None:
        """Delete a tax record"""
        session: Session = self.database.Session()
        try:
            self.logger.info(f"Deleting tax record: username={username}, year={year}")
            tax_record = session.query(TaxModel).filter(
                TaxModel.username == username,
                TaxModel.year == year
            ).first()
            
            if tax_record:
                session.delete(tax_record)
                session.commit()
                self.logger.info("Tax record deleted successfully")
            
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Database error while deleting tax: {str(e)}")
            raise DatabaseException("Failed to delete tax record.", e) from e
        finally:
            session.close()