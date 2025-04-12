from abc import ABC, abstractmethod
from datetime import date
from adapters.models import NavHistoryModel
from typing import BinaryIO

class INavHistoryRepository(ABC):
    @abstractmethod
    def get_nav_history_by_fund_name_and_date(self, fund_name: str, date: date) -> NavHistoryModel:
        pass
    
    @abstractmethod
    def get_all_nav_history_by_fund_name(self, fund_name: str) -> list[NavHistoryModel]:
        pass
        
    @abstractmethod
    def get_nav_history_by_fund_name_and_date_range(self, fund_name: str, start_date: date, end_date: date) -> list[NavHistoryModel]:
        pass
    
    @abstractmethod
    def add_nav_history(self, nav_history: NavHistoryModel) -> None:
        pass
    
    @abstractmethod
    def update_nav_history(self, fund_name: str, date: date, nav_history: NavHistoryModel) -> None:
        pass
            
    @abstractmethod
    def delete_nav_history(self, fund_name: str, date: date) -> None:
        pass

    @abstractmethod
    def delete_nav_history_by_fund(self, fund_name: str) -> None:
        pass
    
    @abstractmethod
    def get_nav_history_latest_date(self, fund_name: str) -> NavHistoryModel:
        pass
    
    @abstractmethod
    def get_nav_history_lastest_date_all_fund(self) -> list[NavHistoryModel]:
        pass

    @abstractmethod
    def get_nav_history_by_date(self, date: date) -> list[NavHistoryModel]:
        pass

    @abstractmethod
    def get_all_nav_history(self) -> list[NavHistoryModel]:
        pass

    @abstractmethod
    def upload_nav_history_file(self, file: BinaryIO) -> None:
        pass