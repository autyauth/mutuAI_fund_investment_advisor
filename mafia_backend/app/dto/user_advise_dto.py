from utils.advise_enum import AdviseEnum
from datetime import datetime
from typing import List, Tuple

class UserAdviseDTO():
    def __init__(self, username: str, date: str, remainingInvestmentNeeded: AdviseEnum, 
                 trend_up_funds: List[str], non_trend_up_funds: List[str], 
                 remain_amount_month: int, remain_amount_year: int, 
                 advise_funds: List[Tuple[str, str]] = None):  # แก้ตรงนี้ให้เป็น List[Tuple[str, str]]
        self.username = username
        self.date = date
        self.remainingInvestmentNeeded = remainingInvestmentNeeded
        self.trend_up_funds = trend_up_funds
        self.non_trend_up_funds = non_trend_up_funds
        self.remain_amount_month = remain_amount_month
        self.remain_amount_year = remain_amount_year
        self.advise_funds = advise_funds if advise_funds is not None else []  # ตรวจสอบค่าเริ่มต้น

    def to_dict(self):
        return {
            "username": self.username,
            "date": self.date,
            "remainingInvestmentNeeded": self.remainingInvestmentNeeded.name if self.remainingInvestmentNeeded else None,
            "trend_up_funds": self.trend_up_funds,
            "non_trend_up_funds": self.non_trend_up_funds,
            "remain_amount_month": float(self.remain_amount_month),
            "remain_amount_year": float(self.remain_amount_year),
            "advise_funds": [{"fund": fund, "action": action} for fund, action in self.advise_funds]  # แปลงเป็น dict
        }
