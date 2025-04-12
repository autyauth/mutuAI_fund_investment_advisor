from adapters.models.performance_mutual_funds_model import PerformanceMutualFundsModel
from datetime import datetime

class PerformanceMutualFundsDTO:
    def __init__(self, fund_name: str, date: datetime, 
                 three_month_roc: float, six_month_roc: float, ytd_roc: float, one_year_roc: float, three_year_roc: float, five_year_roc: float, ten_year_roc: float,
                 std_one_year: float, std_three_year: float, std_five_year: float, std_ten_year: float,
                 sharpe_ratio_one_year: float, sharpe_ratio_three_year: float, sharpe_ratio_five_year: float, sharpe_ratio_ten_year: float):
        self.fund_name = fund_name
        self.date = date
        
        self.three_month_roc = three_month_roc
        self.six_month_roc = six_month_roc
        self.ytd_roc = ytd_roc
        self.one_year_roc = one_year_roc
        self.three_year_roc = three_year_roc
        self.five_year_roc = five_year_roc
        self.ten_year_roc = ten_year_roc
        
        self.std_one_year = std_one_year
        self.std_three_year = std_three_year
        self.std_five_year = std_five_year
        self.std_ten_year = std_ten_year
        
        self.sharpe_ratio_one_year = sharpe_ratio_one_year
        self.sharpe_ratio_three_year = sharpe_ratio_three_year
        self.sharpe_ratio_five_year = sharpe_ratio_five_year
        self.sharpe_ratio_ten_year = sharpe_ratio_ten_year
    
    @staticmethod
    def from_model(model: PerformanceMutualFundsModel, 
                   three_month_roc: float, six_month_roc: float, ytd_roc: float, one_year_roc: float, three_year_roc: float, five_year_roc: float, ten_year_roc: float) -> "PerformanceMutualFundsDTO":
        return PerformanceMutualFundsDTO(
            fund_name=model.fund_name,
            date=model.date,
            
            three_month_roc=round(three_month_roc * 100, 2),
            six_month_roc=round(six_month_roc * 100, 2),
            ytd_roc=round(ytd_roc * 100, 2),
            one_year_roc=round(one_year_roc * 100, 2),
            three_year_roc=round(three_year_roc * 100, 2),
            five_year_roc=round(five_year_roc * 100, 2),
            ten_year_roc=round(ten_year_roc * 100, 2),
            
            std_one_year=round(model.std_one_year * 100, 2),
            std_three_year=round(model.std_three_year * 100, 2),
            std_five_year=round(model.std_five_year * 100, 2),
            std_ten_year=round(model.std_ten_year * 100, 2),
            
            sharpe_ratio_one_year=round(model.sharpe_ratio_one_year, 2),
            sharpe_ratio_three_year=round(model.sharpe_ratio_three_year, 2),
            sharpe_ratio_five_year=round(model.sharpe_ratio_five_year, 2),
            sharpe_ratio_ten_year=round(model.sharpe_ratio_ten_year, 2)
        )
    
    def to_model(self) -> PerformanceMutualFundsModel:
        return PerformanceMutualFundsModel(
            fund_name=self.fund_name,
            date=self.date,
            std_one_year=self.std_one_year,
            std_three_year=self.std_three_year,
            std_five_year=self.std_five_year,
            std_ten_year=self.std_ten_year,
            sharpe_ratio_one_year=self.sharpe_ratio_one_year,
            sharpe_ratio_three_year=self.sharpe_ratio_three_year,
            sharpe_ratio_five_year=self.sharpe_ratio_five_year,
            sharpe_ratio_ten_year=self.sharpe_ratio_ten_year
        )
    
    def to_dict(self):
        return {
            "fund_name": self.fund_name,
            "date": self.date,
            "three_month_roc": self.three_month_roc,
            "six_month_roc": self.six_month_roc,
            "ytd_roc": self.ytd_roc,
            "one_year_roc": self.one_year_roc,
            "three_year_roc": self.three_year_roc,
            "five_year_roc": self.five_year_roc,
            "ten_year_roc": self.ten_year_roc,
            "std_one_year": self.std_one_year,
            "std_three_year": self.std_three_year,
            "std_five_year": self.std_five_year,
            "std_ten_year": self.std_ten_year,
            "sharpe_ratio_one_year": self.sharpe_ratio_one_year,
            "sharpe_ratio_three_year": self.sharpe_ratio_three_year,
            "sharpe_ratio_five_year": self.sharpe_ratio_five_year,
            "sharpe_ratio_ten_year": self.sharpe_ratio_ten_year
        }