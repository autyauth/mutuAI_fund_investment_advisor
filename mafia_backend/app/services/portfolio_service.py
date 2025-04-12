from services.exceptions import BusinessLogicException
from adapters.repositories.portfolio_repository import PortfolioRepository
import logging

from decimal import Decimal

class PortfolioService:
    def __init__(self, portfolio_repository: PortfolioRepository):

        self.portfolio_repository = portfolio_repository
        self.logger = logging.getLogger(__name__)
        
    def update_gain_loss_and_nav_present(self, fund_name:str, nav_today:float):
        portfolios = self.portfolio_repository.get_all_portfolio_by_fund_name(fund_name)
        nav_today = Decimal(str(nav_today))
        if not portfolios:
            return
        for portfolio in portfolios:
            # update present_nav and gain_loss
            # update present_nav
            portfolio.present_nav = nav_today
            # update gain_loss
            portfolio.gain_loss_value = (nav_today * portfolio.holding_units) - portfolio.cost
            portfolio.gain_loss_percent = (nav_today/portfolio.nav_average - 1) * 100

            # update portfolio
            self.portfolio_repository.update_portfolio(portfolio.username, fund_name,portfolio)
        
        

    def get_all_portfolio_by_username(self, username: str):
        portfolios = self.portfolio_repository.get_all_portfolio_by_username(username)
        if not portfolios:
            return []
        return [self._portfolio_to_dto(p) for p in portfolios]

    def _portfolio_to_dto(self, portfolio):
        return {
            'fund_name': portfolio.fund_name,
            'fund_type': portfolio.fund_type,
            'holding_units': float(portfolio.holding_units),
            'holding_value': float(portfolio.holding_value),
            'cost': float(portfolio.cost),
            'nav_average': float(portfolio.nav_average),
            'present_nav': float(portfolio.present_nav),
            'total_profit': float(portfolio.total_profit),
            'gain_loss_percent': float(portfolio.gain_loss_percent),
            'gain_loss_value': float(portfolio.gain_loss_value),
            'valid_units': float(portfolio.valid_units)
        }
    
    # portfolio_service.py
    def get_portfolio_by_year(self, username: str, year: int):
        try:
            self.logger.info(f"Service: Getting portfolio for user {username} year {year}")
            portfolios = self.portfolio_repository.get_portfolio_by_year(username, year)
            
            # Add debug logging
            self.logger.debug(f"Raw portfolio data from repository: {portfolios}")
            
            if not portfolios:
                self.logger.info(f"No portfolio found for user {username} in year {year}")
                return []
                
            result = [self._portfolio_to_dto(p) for p in portfolios]
            self.logger.debug(f"Converted portfolio data: {result}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error getting portfolio for year {year}: {str(e)}", exc_info=True)
            raise BusinessLogicException(f"Failed to get portfolio: {str(e)}")