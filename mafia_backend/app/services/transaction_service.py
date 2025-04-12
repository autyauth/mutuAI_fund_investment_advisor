from datetime import date
from typing import Optional
from decimal import Decimal
from services.exceptions import BusinessLogicException
from dto.transaction_dto import TransactionDTO, TransactionType
from dto.fund_type_enum import FundType
from adapters.models import PortfolioModel
# from adapters.repositories.nav_history_repository import NavHistoryRepository
import logging
from datetime import datetime

class TransactionService:
   def __init__(self, transaction_repository, nav_history_repository, portfolio_repository, user_repository, goal_repository):
        self.transaction_repository = transaction_repository
        self.nav_history_repository = nav_history_repository
        self.portfolio_repository = portfolio_repository
        self.user_repository = user_repository
        self.goal_repository = goal_repository
        self.logger = logging.getLogger(__name__)

   def calculate_transaction_gain_loss(self, transaction_type: TransactionType, 
                                    fund_name: str,
                                    units: float, 
                                    processed_nav: float, 
                                    portfolio: Optional[PortfolioModel] = None):
       try:
           # Get latest market NAV for comparison
           latest_nav = self.nav_history_repository.get_nav_history_latest_date(fund_name)
           if not latest_nav:
               raise BusinessLogicException("Cannot find latest NAV for the fund")

           if transaction_type == TransactionType.BUY:
               # Calculate unrealized gain/loss based on current market price
               market_value = units * float(latest_nav.nav)
               invested_value = units * processed_nav
               gain_loss_value = market_value - invested_value
               gain_loss_percent = (gain_loss_value / invested_value) * 100 if invested_value != 0 else 0
               
               return gain_loss_percent, gain_loss_value
               
           else:  # SELL - Realized gain/loss
               if not portfolio:
                   raise BusinessLogicException("Portfolio required for sell transactions")
                   
               # Calculate realized gain/loss based on average cost
               avg_cost = float(portfolio.cost) / float(portfolio.holding_units)
               invested_value = units * avg_cost
               sell_value = units * processed_nav
               gain_loss_value = sell_value - invested_value
               gain_loss_percent = (gain_loss_value / invested_value) * 100 if invested_value != 0 else 0
               
               return gain_loss_percent, gain_loss_value
               
       except Exception as e:
           self.logger.error(f"Error calculating gain/loss: {str(e)}")
           raise BusinessLogicException(f"Failed to calculate gain/loss: {str(e)}")

   def get_transactions_by_username(self, username: str):
       try:
           self.logger.info(f"Service: Getting transactions for user {username}")
           transactions = self.transaction_repository.get_transactions_by_username(username)
           if not transactions:
               return []
               
           result = []
           for tx in transactions:
               try:
                   dto = self._transaction_to_dto(tx)
                   result.append(dto)
               except Exception as e:
                   self.logger.error(f"Error converting transaction to DTO: {str(e)}")
                   continue
                   
           return result
           
       except Exception as e:
           self.logger.error(f"Error in get_transactions_by_username: {str(e)}")
           raise BusinessLogicException(f"Failed to get transactions: {str(e)}")

   def process_buy_transaction(self, transaction_dto: TransactionDTO) -> None:
       try:
           user = self.user_repository.get_user(transaction_dto.username)
           if not user:
               raise BusinessLogicException("User not found")
           
           transaction_year = transaction_dto.transaction_date.year
           gain_loss_percent, gain_loss_value = self.calculate_transaction_gain_loss(
                TransactionType.BUY,
                transaction_dto.fund_name,
                float(transaction_dto.units_processed),
                float(transaction_dto.processed_nav)
            )

           transaction_id = self.transaction_repository.create_transaction(
                username=transaction_dto.username,
                fund_name=transaction_dto.fund_name,
                transaction_type=TransactionType.BUY.value,
                transaction_date=transaction_dto.transaction_date,
                units_processed=float(transaction_dto.units_processed),
                amount_processed=float(transaction_dto.amount_processed),
                processed_nav=float(transaction_dto.processed_nav),
                gain_loss_percent=gain_loss_percent,
                gain_loss_value=gain_loss_value
            )

           if (transaction_dto.fund_type == FundType.RMF or transaction_dto.fund_type == FundType.SSF)and datetime.now().year == transaction_year: # ต้องเพิ่มทุกอัน
               self.goal_repository.update_investment_amounts(
                   username=transaction_dto.username,
                   year=transaction_year,
                   fund_type=transaction_dto.fund_type.value,
                   amount=float(transaction_dto.amount_processed)
               )
           elif transaction_dto.fund_type == FundType.SSF and datetime.now().year == transaction_year and transaction_dto.amount_processed < 0:
               self.goal_repository.update_investment_amounts(
                   username=transaction_dto.username,
                   year=transaction_year,
                   fund_type=transaction_dto.fund_type.value,
                   amount=float(transaction_dto.amount_processed)
               )
           
           existing_portfolio = self.portfolio_repository.get_portfolio(
               transaction_dto.username, 
               transaction_dto.fund_name
           )


           if existing_portfolio:
               latest_nav = float(self.nav_history_repository.get_nav_history_latest_date(transaction_dto.fund_name).nav)
               new_valid_units = float(existing_portfolio.valid_units) + float(transaction_dto.units_processed)
               holding_units_tmp = float(existing_portfolio.holding_units) + float(transaction_dto.units_processed)
               cost_tmp = float(existing_portfolio.cost) + float(transaction_dto.amount_processed)
               gl_value_tmp = (holding_units_tmp * latest_nav) - cost_tmp
               new_portfolio = PortfolioModel(
                   username=transaction_dto.username,
                   fund_name=transaction_dto.fund_name,
                   fund_type=transaction_dto.fund_type.value,
                   holding_units=holding_units_tmp,
                   holding_value= holding_units_tmp * latest_nav,
                   cost= cost_tmp,
                   nav_average= (cost_tmp) / (holding_units_tmp),
                   present_nav= latest_nav,
                   total_profit=float(existing_portfolio.total_profit),
                   gain_loss_percent = float(((gl_value_tmp + cost_tmp) / cost_tmp) - 1.0) * 100.0,
                   gain_loss_value=gl_value_tmp,
                   valid_units=new_valid_units
               )
               self.portfolio_repository.update_portfolio(
                   username=transaction_dto.username,
                   fund_name=transaction_dto.fund_name,
                   portfolio=new_portfolio
               )
           else:
               latest_nav = float(self.nav_history_repository.get_nav_history_latest_date(transaction_dto.fund_name).nav)
               new_portfolio = PortfolioModel(
                   username=transaction_dto.username,
                   fund_name=transaction_dto.fund_name,
                   fund_type=transaction_dto.fund_type.value,
                   holding_units=float(transaction_dto.units_processed),
                   holding_value=float(transaction_dto.units_processed * latest_nav),
                   cost=float(transaction_dto.amount_processed),
                   nav_average=float(transaction_dto.processed_nav),
                   present_nav=latest_nav,
                   total_profit=0.0,
                   gain_loss_percent=gain_loss_percent,
                   gain_loss_value=gain_loss_value,
                   valid_units=float(transaction_dto.amount_processed)
               )
               self.portfolio_repository.create_portfolio(new_portfolio)
       except Exception as e:
           self.logger.error(f"Error in buy transaction: {str(e)}")
           raise BusinessLogicException(f"Failed to process buy transaction: {str(e)}")

   def process_sell_transaction(self, transaction_dto: TransactionDTO) -> None:
       try:
           existing_portfolio = self.portfolio_repository.get_portfolio(
               transaction_dto.username, 
               transaction_dto.fund_name
           )
           if not existing_portfolio:
               raise BusinessLogicException("No portfolio found for this fund")

           if float(existing_portfolio.holding_units) < float(transaction_dto.units_processed):
               raise BusinessLogicException(f"Insufficient units. Available: {existing_portfolio.holding_units}")

           gain_loss_percent, gain_loss_value = self.calculate_transaction_gain_loss(
               TransactionType.SELL,
               transaction_dto.fund_name,
               float(transaction_dto.units_processed),
               float(transaction_dto.processed_nav),
               existing_portfolio
           )

           transaction_id = self.transaction_repository.create_transaction(
               username=transaction_dto.username,
               fund_name=transaction_dto.fund_name,
               transaction_type=TransactionType.SELL.value,
               transaction_date=transaction_dto.transaction_date,
               units_processed=float(transaction_dto.units_processed),
               amount_processed=float(transaction_dto.amount_processed),
               processed_nav=float(transaction_dto.processed_nav),
               gain_loss_percent=gain_loss_percent,
               gain_loss_value=gain_loss_value
           )
           transaction_year = transaction_dto.transaction_date.year
           if (transaction_dto.fund_type == FundType.RMF or transaction_dto.fund_type == FundType.SSF)and datetime.now().year == transaction_year: # ต้องเพิ่มทุกอัน
               self.goal_repository.update_investment_amounts(
                   username=transaction_dto.username,
                   year=transaction_year,
                   fund_type=transaction_dto.fund_type.value,
                   amount=-float(transaction_dto.amount_processed)
               )
           elif transaction_dto.fund_type == FundType.SSF and datetime.now().year == transaction_year and transaction_dto.amount_processed < 0:
               self.goal_repository.update_investment_amounts(
                   username=transaction_dto.username,
                   year=transaction_year,
                   fund_type=transaction_dto.fund_type.value,
                   amount=-float(transaction_dto.amount_processed)
               )

           new_valid_units = float(existing_portfolio.valid_units) - float(transaction_dto.amount_processed)
           new_holding_units = float(existing_portfolio.holding_units) - float(transaction_dto.units_processed)
           new_holding_value = new_holding_units * float(transaction_dto.processed_nav)
           
           if new_holding_units <= 0:
               self.portfolio_repository.delete_portfolio(
                   username=transaction_dto.username,
                   fund_name=transaction_dto.fund_name
               )
           else:
               new_cost = float(existing_portfolio.cost) * (new_holding_units / float(existing_portfolio.holding_units))
               new_nav_average = new_cost / new_holding_units if new_holding_units > 0 else 0
               new_total_profit = float(existing_portfolio.total_profit) + gain_loss_value

               new_portfolio = PortfolioModel(
                   username=transaction_dto.username,
                   fund_name=transaction_dto.fund_name,
                   fund_type=FundType.RMF.value,
                   holding_units=new_holding_units,
                   holding_value=new_holding_value,
                   cost=new_cost,
                   nav_average=new_nav_average,
                   present_nav=float(transaction_dto.processed_nav),
                   total_profit=new_total_profit,
                   gain_loss_percent=gain_loss_percent,
                   gain_loss_value=gain_loss_value,
                   valid_units=new_valid_units
               )
               self.portfolio_repository.update_portfolio(
                   username=transaction_dto.username,
                   fund_name=transaction_dto.fund_name,
                   portfolio=new_portfolio
               )
       except Exception as e:
           self.logger.error(f"Error in sell transaction: {str(e)}")
           raise BusinessLogicException(f"Failed to process sell transaction: {str(e)}")

   def _transaction_to_dto(self, transaction):
       try:
           return {
               'transaction_id': transaction.transaction_id,
               'username': transaction.username,
               'fund_name': transaction.fund_name,
               'transaction_type': transaction.transaction_type,
               'transaction_date': transaction.transaction_date.isoformat() if transaction.transaction_date else None,
               'units_processed': float(transaction.units_processed) if transaction.units_processed else 0,
               'amount_processed': float(transaction.amount_processed) if transaction.amount_processed else 0,
               'processed_nav': float(transaction.processed_nav) if transaction.processed_nav else 0,
               'gain_loss_percent': float(transaction.gain_loss_percent) if transaction.gain_loss_percent else 0,
               'gain_loss_value': float(transaction.gain_loss_value) if transaction.gain_loss_value else 0,
               'valid_to_sell': transaction.valid_to_sell.isoformat() if transaction.valid_to_sell else None
           }
       except Exception as e:
           self.logger.error(f"Error in _transaction_to_dto: {str(e)}")
           raise