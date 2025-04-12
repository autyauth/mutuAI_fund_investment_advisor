# app/adapters/repositories/interfaces/ITransaction_repository.py
from abc import ABC, abstractmethod
from datetime import date

class ITransactionRepository(ABC):
    @abstractmethod
    def create_transaction(self, username: str, fund_name: str, transaction_type: int,
                         transaction_date: date, units_processed: float, amount_processed: float,
                         processed_nav: float, gain_loss_percent: float, gain_loss_value: float) -> int:
        pass

    @abstractmethod
    def get_transactions_by_username(self, username: str) -> list:
        pass

    @abstractmethod
    def get_transaction_by_id(self, transaction_id: int):
        pass