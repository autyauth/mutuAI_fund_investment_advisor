from dto.performance_mutual_funds_dto import PerformanceMutualFundsDTO

class HomeReccomentFundsDTO(PerformanceMutualFundsDTO):
    def __init__(self, fund_risk:str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fund_risk = fund_risk
    
    def to_dict(self):
        return {
            **super().to_dict(),
            "fund_risk": self.fund_risk
        }