from abc import ABC, abstractmethod
from adapters.models import MutualFundModel

class IMutualFundRepository(ABC):
    @abstractmethod
    def get_all_mutual_funds(self) -> list[MutualFundModel]:
        pass

    @abstractmethod
    def get_mutual_fund_by_name(self, fund_name: str) -> MutualFundModel:
        pass