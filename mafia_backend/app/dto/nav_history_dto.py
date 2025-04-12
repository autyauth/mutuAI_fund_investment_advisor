from adapters.models import NavHistoryModel
from datetime import date

class NavHistoryDTO:
    def __init__(self, fund_name: str, date: date, nav: float, fund_type: str, selling_price: float, redemption_price: float, total_net_assets: float, change: float):
        self.fund_name = fund_name
        self.date = date
        self.nav = nav
        self.fund_type = fund_type
        self.selling_price = selling_price
        self.redemption_price = redemption_price
        self.total_net_assets = total_net_assets
        self.change = change

    @staticmethod
    def from_model(model: NavHistoryModel) -> "NavHistoryDTO":
        return NavHistoryDTO(
            fund_name=model.fund_name,
            date=model.date,
            nav=model.nav,
            fund_type=model.fund_type,
            selling_price=model.selling_price,
            redemption_price=model.redemption_price,
            total_net_assets=model.total_net_assets,
            change=model.change
        )

    def to_model(self) -> NavHistoryModel:
        return NavHistoryModel(
            fund_name=self.fund_name,
            date=self.date,
            nav=self.nav,
            fund_type=self.fund_type,
            selling_price=self.selling_price,
            redemption_price=self.redemption_price,
            total_net_assets=self.total_net_assets,
            change=self.change
        )

    def to_dict(self):
        return {
            "fund_name": self.fund_name,
            "date": self.date,
            "nav": self.nav,
            "fund_type": self.fund_type,
            "selling_price": self.selling_price,
            "redemption_price": self.redemption_price,
            "total_net_assets": self.total_net_assets,
            "change": self.change
        }