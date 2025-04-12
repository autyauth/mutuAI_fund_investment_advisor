from adapters.models.prediction_trend_funds_model import PredictionTrendFundsModel

class PredictionTrendFundsDTO:
    def __init__(self, fund_name: str, date: str, trend: int, up_trend_prob: float, down_trend_prob: float, reason: str, indicator: str):
        self.fund_name = fund_name
        self.date = date
        self.trend = trend
        self.up_trend_prob = up_trend_prob
        self.down_trend_prob = down_trend_prob
        self.reason = reason
        self.indicator = indicator

    @staticmethod
    def from_model(model: PredictionTrendFundsModel) -> "PredictionTrendFundsDTO":
        return PredictionTrendFundsDTO(
            fund_name=model.fund_name,
            date=model.date,
            trend=model.trend,
            up_trend_prob=model.up_trend_prob,
            down_trend_prob=model.down_trend_prob,
            reason=model.reason,
            indicator=model.indicator
        )
    def to_model(self) -> PredictionTrendFundsModel:
        return PredictionTrendFundsModel(
            fund_name=self.fund_name,
            date=self.date,
            trend=self.trend,
            up_trend_prob=self.up_trend_prob,
            down_trend_prob=self.down_trend_prob,
            reason=self.reason,
            indicator=self.indicator
        )
    def to_dict(self):
        return {
            "fund_name": self.fund_name,
            "date": self.date,
            "trend": self.trend,
            "up_trend_prob": self.up_trend_prob,
            "down_trend_prob": self.down_trend_prob,
            "reason": self.reason,
            "indicator": self.indicator
        }