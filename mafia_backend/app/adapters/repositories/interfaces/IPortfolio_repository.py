from abc import ABC, abstractmethod
from adapters.models import PortfolioModel

class IPortfolioRepository(ABC):
    @abstractmethod
    def get_portfolio(self, username: str, fund_name: str) -> PortfolioModel:
        pass

    @abstractmethod
    def get_all_portfolio_by_username(self, username: str) -> list[PortfolioModel]:
        pass

    @abstractmethod
    def create_portfolio(self, portfolio: PortfolioModel) -> None:
        pass

    @abstractmethod
    def update_portfolio(self, username: str, fund_name: str, portfolio: PortfolioModel) -> None:
        pass

    @abstractmethod
    def delete_portfolio(self, username: str, fund_name: str) -> None:
        pass

    @abstractmethod
    def delete_portfolio_by_username(self, username: str) -> None:
        pass