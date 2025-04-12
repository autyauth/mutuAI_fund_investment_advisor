from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import text
from adapters.repositories.interfaces.IPortfolio_repository import IPortfolioRepository
from adapters.models import PortfolioModel
from adapters.exceptions import *
from datetime import date
import logging

class PortfolioRepository(IPortfolioRepository):
    def __init__(self, database):
        self.database = database
        self.logger = logging.getLogger(__name__)

    def get_portfolio(self, username: str, fund_name: str) -> PortfolioModel:
        session: Session = self.database.Session()
        try:
            portfolio = (
                session.query(PortfolioModel)
                .filter(
                    PortfolioModel.username == username,
                    PortfolioModel.fund_name == fund_name
                )
                .first()
            )
            return portfolio
        except SQLAlchemyError as e:
            raise DatabaseException("Failed to retrieve portfolio.", e) from e
        finally:
            session.close()

    def get_all_portfolio_by_username(self, username: str) -> list[PortfolioModel]:
        session: Session = self.database.Session()
        try:
            portfolios = (
                session.query(PortfolioModel)
                .filter(PortfolioModel.username == username)
                .all()
            )
            return portfolios
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving portfolios: {str(e)}")
            raise DatabaseException("Failed to retrieve portfolios", e)
        finally:
            session.close()
    
    def get_all_portfolio_by_fund_name(self, fund_name: str) -> list[PortfolioModel]:
        session: Session = self.database.Session()
        try:
            portfolios = (
                session.query(PortfolioModel)
                .filter(PortfolioModel.fund_name == fund_name)
                .all()
            )
            return portfolios
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving portfolios: {str(e)}")
            raise DatabaseException("Failed to retrieve portfolios", e)
        finally:
            session.close()

    def create_portfolio(self, portfolio: PortfolioModel) -> None:
        session: Session = self.database.Session()
        try:
            session.add(portfolio)
            session.commit()
        except IntegrityError as e:
            session.rollback()
            if "duplicate" in str(e.orig).lower():
                raise DuplicateEntryException(
                    f"Portfolio already exists for user {portfolio.username} and fund {portfolio.fund_name}", e
                ) from e
            raise DatabaseException("Integrity error occurred while creating portfolio.", e) from e
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseException("Failed to create portfolio.", e) from e
        finally:
            session.close()

    def update_portfolio(self, username: str, fund_name: str, portfolio: PortfolioModel) -> None:
        session: Session = self.database.Session()
        try:
            existed_portfolio = (
                session.query(PortfolioModel)
                .filter(
                    PortfolioModel.username == username,
                    PortfolioModel.fund_name == fund_name
                )
                .first()
            )
            
            if existed_portfolio is None:
                raise RecordNotFoundException(
                    f"Portfolio for user '{username}' and fund '{fund_name}' not found for update."
                )

            # Update all non-None attributes
            for attr, value in portfolio.__dict__.items():
                if not attr.startswith("_") and value is not None:
                    setattr(existed_portfolio, attr, value)
            
            session.commit()
        except RecordNotFoundException as e:
            session.rollback()
            raise
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseException("Failed to update portfolio.", e) from e
        finally:
            session.close()

    def delete_portfolio(self, username: str, fund_name: str) -> None:
        session: Session = self.database.Session()
        try:
            portfolio = (
                session.query(PortfolioModel)
                .filter(
                    PortfolioModel.username == username,
                    PortfolioModel.fund_name == fund_name
                )
                .first()
            )
            
            if portfolio is None:
                raise RecordNotFoundException(
                    f"Portfolio for user '{username}' and fund '{fund_name}' not found for deletion."
                )
            
            session.delete(portfolio)
            session.commit()
        except RecordNotFoundException as e:
            session.rollback()
            raise
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseException("Failed to delete portfolio.", e) from e
        finally:
            session.close()

    def delete_portfolio_by_username(self, username: str) -> None:
        session: Session = self.database.Session()
        try:
            session.execute(
                text("DELETE FROM portfolio WHERE username = :username"),
                {"username": username}
            )
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseException("Failed to delete portfolios by username.", e) from e
        finally:
            session.close()

    def get_portfolio_by_year(self, username: str, year: int) -> list[PortfolioModel]:
        session: Session = self.database.Session()
        try:
            # Join with mutual_funds table to get fund_type
            sql_query = """
                SELECT 
                    t.fund_name,
                    m.fund_type,  # Get fund_type from mutual_funds table
                    SUM(CASE 
                        WHEN t.transaction_type = 1 THEN t.units_processed
                        WHEN t.transaction_type = 2 THEN -t.units_processed
                        ELSE 0 
                    END) as holding_units,
                    SUM(CASE 
                        WHEN t.transaction_type = 1 THEN t.amount_processed
                        WHEN t.transaction_type = 2 THEN -t.amount_processed
                        ELSE 0 
                    END) as cost,
                    SUM(t.gain_loss_value) as total_profit
                FROM transactions t
                INNER JOIN mutual_funds m ON t.fund_name = m.fund_name  # Add this join
                WHERE t.username = :username 
                AND YEAR(t.transaction_date) = :year
                GROUP BY t.fund_name, m.fund_type  # Include m.fund_type in GROUP BY
                HAVING holding_units > 0
            """
            
            print(f"Executing query with params: username={username}, year={year}")
            
            transactions = session.execute(text(sql_query), {
                "username": username,
                "year": year
            }).fetchall()
            
            print(f"Found {len(transactions) if transactions else 0} transactions")

            if not transactions:
                return []

            portfolios = []
            for tx in transactions:
                nav_query = """
                    SELECT nav
                    FROM nav_history
                    WHERE fund_name = :fund_name
                    ORDER BY date DESC
                    LIMIT 1
                """
                
                latest_nav = session.execute(
                    text(nav_query),
                    {"fund_name": tx.fund_name}
                ).scalar()
                
                print(f"Latest NAV for {tx.fund_name}: {latest_nav}")

                if latest_nav:
                    # Convert all numeric values to float before calculations
                    holding_units = float(tx.holding_units)
                    cost = float(tx.cost)
                    total_profit = float(tx.total_profit)
                    latest_nav_float = float(latest_nav)

                    # Calculate values after conversion
                    holding_value = holding_units * latest_nav_float
                    nav_average = cost / holding_units if holding_units > 0 else 0
                    gain_loss_percent = (total_profit / cost * 100) if cost > 0 else 0

                    portfolio = PortfolioModel(
                        username=username,
                        fund_name=tx.fund_name,
                        fund_type=tx.fund_type,
                        holding_units=holding_units,
                        holding_value=holding_value,
                        cost=cost,
                        nav_average=nav_average,
                        present_nav=latest_nav_float,
                        total_profit=total_profit,
                        gain_loss_percent=gain_loss_percent,
                        gain_loss_value=total_profit,
                        valid_units=holding_units
                    )
                    portfolios.append(portfolio)
                    print(f"Added portfolio entry for {tx.fund_name}")

            return portfolios

        except Exception as e:
            print(f"Error in get_portfolio_by_year: {str(e)}")
            self.logger.error(f"Error in get_portfolio_by_year: {str(e)}", exc_info=True)
            raise DatabaseException("Failed to retrieve portfolio by year", e)
        finally:
            session.close()
            
    def get_funds_from_portfolio_by_username_holding_units(self, username: str,) -> list[str]:
        session: Session = self.database.Session()
        try:
            funds = (
                session.query(PortfolioModel.fund_name)
                .filter(
                    PortfolioModel.username == username,
                    PortfolioModel.fund_type == "RMF",
                    PortfolioModel.holding_units > 0
                )
                .all()
            )
            return [fund.fund_name for fund in funds]
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving funds: {str(e)}")
            raise DatabaseException("Failed to retrieve funds", e)
        finally:
            session.close()