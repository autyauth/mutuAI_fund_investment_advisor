from adapters.models.mutual_fund_model import MutualFundModel

class MutualFundDTO:
    def __init__(self, fund_name: str, category: str, securities_industry: str, fund_type: str, fund_risk: str):
        self.fund_name = fund_name
        self.category = category
        self.securities_industry = securities_industry
        self.fund_type = fund_type
        self.fund_risk = fund_risk

    @staticmethod
    def from_model(model: MutualFundModel) -> "MutualFundDTO":
        return MutualFundDTO(
            fund_name=model.fund_name,
            category=model.category,
            securities_industry=model.securities_industry,
            fund_type=model.fund_type,
            fund_risk=model.fund_risk
        )

    def to_model(self) -> MutualFundModel:
        return MutualFundModel(
            fund_name=self.fund_name,
            category=self.category,
            securities_industry=self.securities_industry,
            fund_type=self.fund_type,
            fund_risk=self.fund_risk
        )

    def to_dict(self):
        return {
            "fund_name": self.fund_name,
            "category": self.category,
            "securities_industry": self.securities_industry,
            "fund_type": self.fund_type,
            "fund_risk": self.fund_risk
        }
