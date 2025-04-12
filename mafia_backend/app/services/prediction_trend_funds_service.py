from adapters.repositories.prediction_trend_funds_repository import PredictionTrendFundsRepository
from adapters.models.prediction_trend_funds_model import PredictionTrendFundsModel
from dto.prediction_trend_funds_dto import PredictionTrendFundsDTO

from adapters.repositories.transaction_repository import TransactionRepository
from adapters.models.transaction_model import TransactionModel

from adapters.repositories.goal_repository import GoalRepository
from adapters.models.goal_model import GoalModel

from adapters.repositories.user_repository import UserRepository
from adapters.models.user_model import UserModel

from pendulum import timezone
import pendulum
from dateutil.relativedelta import relativedelta, FR

class PredictionTrendFundsService:
    def __init__(self, prediction_trend_funds_repository: PredictionTrendFundsRepository, 
                 transaction_repository: TransactionRepository,
                 goal_repository: GoalRepository,
                 user_repository: UserRepository):
        self.prediction_trend_funds_repository = prediction_trend_funds_repository
        self.transaction_repository = transaction_repository
        self.goal_repository = goal_repository
        self.user_repository = user_repository
        

    def get_prediction_trend_funds(self, fund_name: str, date: str) -> PredictionTrendFundsDTO:
        prediction_trend_funds = self.prediction_trend_funds_repository.get_prediction_trend_funds(fund_name, date)
        return PredictionTrendFundsDTO.from_model(prediction_trend_funds)

    def get_mutual_all_prediction_trend_funds(self, fund_name: str) -> list[PredictionTrendFundsDTO]:
        prediction_trend_funds = self.prediction_trend_funds_repository.get_mutual_all_prediction_trend_funds(fund_name)
        return [PredictionTrendFundsDTO.from_model(prediction_trend_fund) for prediction_trend_fund in prediction_trend_funds]
    
    def get_prediction_trend_funds_lastest(self, fund_name: str) -> PredictionTrendFundsDTO:
        prediction_trend_funds = self.prediction_trend_funds_repository.get_prediction_trend_funds_lastest(fund_name)
        return PredictionTrendFundsDTO.from_model(prediction_trend_funds)
    
    def get_prediction_trend_funds_lastest_all(self) -> list[PredictionTrendFundsDTO]:
        prediction_trend_funds = self.prediction_trend_funds_repository.get_prediction_trend_funds_lastest_all()
        return [PredictionTrendFundsDTO.from_model(prediction_trend_fund) for prediction_trend_fund in prediction_trend_funds]

    def get_prediction_trend_by_fund_name_and_date_range(self, fund_name: str, start_date: str, end_date: str) -> list[PredictionTrendFundsDTO]:
        prediction_trend_funds = self.prediction_trend_funds_repository.get_prediction_trend_by_fund_name_and_date_range(fund_name, start_date, end_date)
        return [PredictionTrendFundsDTO.from_model(prediction_trend_fund) for prediction_trend_fund in prediction_trend_funds]
    
    def add_prediction_trend_funds(self, prediction_trend_funds: PredictionTrendFundsDTO) -> PredictionTrendFundsDTO:
        model = prediction_trend_funds.to_model()
        self.prediction_trend_funds_repository.create_or_update_prediction_trend_funds(model)
        return PredictionTrendFundsDTO.from_model(model)
        
        
    