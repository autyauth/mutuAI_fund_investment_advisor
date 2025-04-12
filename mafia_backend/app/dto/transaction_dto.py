# dto/transaction_dto.py
from dataclasses import dataclass
from datetime import date
from enum import Enum
from .fund_type_enum import FundType

class TransactionType(Enum):
    BUY = 1
    SELL = 2

@dataclass
class TransactionDTO:
    username: str
    fund_name: str
    transaction_type: TransactionType
    transaction_date: date
    units_processed: float
    amount_processed: float
    processed_nav: float
    fund_type: FundType = FundType.RMF  # Default to RMF