from datetime import date
from services.exceptions import BusinessLogicException
from adapters.repositories.nav_history_repository import NavHistoryRepository
import logging
from adapters.models.nav_history_model import NavHistoryModel
from dto.nav_history_dto import NavHistoryDTO

class NavHistoryService:
    def __init__(self, nav_history_repository: NavHistoryRepository):
        self.nav_history_repository = nav_history_repository
        self.logger = logging.getLogger(__name__)

    def get_nav_history_lastest_date_all_fund(self):
        try:
            nav_histories = self.nav_history_repository.get_nav_history_lastest_date_all_fund()
            return [self._nav_history_to_dto(nav) for nav in nav_histories]
        except Exception as e:
            self.logger.error(f"Error getting latest NAV for all funds: {str(e)}")
            raise BusinessLogicException(f"Failed to get latest NAV: {str(e)}")

    def get_all_nav_history_by_fund_name(self, fund_name: str):
        try:
            nav_histories = self.nav_history_repository.get_all_nav_history_by_fund_name(fund_name)
            return [self._nav_history_to_dto(nav) for nav in nav_histories]
        except Exception as e:
            self.logger.error(f"Error getting NAV history for fund {fund_name}: {str(e)}")
            raise BusinessLogicException(f"Failed to get NAV history: {str(e)}")

    def get_nav_history_by_date(self, date: date):
        try:
            nav_histories = self.nav_history_repository.get_nav_history_by_date(date)
            return [self._nav_history_to_dto(nav) for nav in nav_histories]
        except Exception as e:
            self.logger.error(f"Error getting NAV history for date {date}: {str(e)}")
            raise BusinessLogicException(f"Failed to get NAV history: {str(e)}")

    def get_nav_history_by_fund_name_and_date(self, fund_name: str, date: date):
        try:
            nav_history = self.nav_history_repository.get_nav_history_by_fund_name_and_date(fund_name, date)
            return self._nav_history_to_dto(nav_history) if nav_history else None
        except Exception as e:
            self.logger.error(f"Error getting NAV history for fund {fund_name} on date {date}: {str(e)}")
            raise BusinessLogicException(f"Failed to get NAV history: {str(e)}")

    def get_all_nav_history(self):
        try:
            nav_histories = self.nav_history_repository.get_all_nav_history()
            return [self._nav_history_to_dto(nav) for nav in nav_histories]
        except Exception as e:
            self.logger.error(f"Error getting all NAV history: {str(e)}")
            raise BusinessLogicException(f"Failed to get NAV history: {str(e)}")

    def _nav_history_to_dto(self, nav_history):
        return {
            'fund_name': nav_history.fund_name,
            'date': nav_history.date.isoformat(),
            'nav': float(nav_history.nav),
            'fund_type': nav_history.fund_type,
            'selling_price': float(nav_history.selling_price) if nav_history.selling_price else None,
            'redemption_price': float(nav_history.redemption_price) if nav_history.redemption_price else None,
            'total_net_assets': float(nav_history.total_net_assets) if nav_history.total_net_assets else None,
            'change': float(nav_history.change) if nav_history.change else None
        }
    
    # In nav_history_service.py

    def get_nav_history_lastest_date_all_fund(self):
        try:
            self.logger.info("Getting latest NAV for all funds")
            nav_histories = self.nav_history_repository.get_nav_history_lastest_date_all_fund()
            if not nav_histories:
                self.logger.info("No NAV histories found")
                return []
            return [self._nav_history_to_dto(nav) for nav in nav_histories]
        except Exception as e:
            self.logger.error(f"Detailed error getting latest NAV: {str(e)}")
            raise BusinessLogicException(f"Failed to get latest NAV: {str(e)}")
    
    def add_nav_history(self, nav_history: NavHistoryModel) -> None:
        try:
            self.logger.info("Adding new NAV history")
            self.nav_history_repository.create_or_update_nav_history(nav_history)
            return NavHistoryDTO.from_model(nav_history)
        except Exception as e:
            self.logger.error(f"Error adding new NAV history: {str(e)}")
            raise BusinessLogicException(f"Failed to add new NAV history: {str(e)}")
        
    def get_nav_history_by_date_range(self, fund_name:str ,start_date: date, end_date: date):
        try:
            self.logger.info(f"Getting NAV history from {start_date} to {end_date}")
            nav_histories = self.nav_history_repository.get_nav_history_by_fund_name_and_date_range(fund_name,start_date, end_date)
            if not nav_histories:
                self.logger.info("No NAV histories found")
                return []
            return [self._nav_history_to_dto(nav) for nav in nav_histories]
        except Exception as e:
            self.logger.error(f"Detailed error getting NAV history by date range: {str(e)}")
            raise BusinessLogicException(f"Failed to get NAV history: {str(e)}")
    
    def get_nav_history_by_fund_name_and_window(self, fund_name: str, window: int):
        try:
            self.logger.info(f"Getting NAV history for fund: {fund_name} with window: {window}")
            nav_histories = self.nav_history_repository.get_nav_history_by_fund_name_and_window(fund_name, window)
            if not nav_histories:
                self.logger.info("No NAV histories found")
                return []
            return [self._nav_history_to_dto(nav) for nav in nav_histories]
        except Exception as e:
            self.logger.error(f"Detailed error getting NAV history by fund and window: {str(e)}")
            raise BusinessLogicException(f"Failed to get NAV history: {str(e)}")