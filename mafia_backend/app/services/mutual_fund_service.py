from services.exceptions import BusinessLogicException
from adapters.repositories.mutual_fund_repository import MutualFundRepository
import logging

class MutualFundService:
    def __init__(self, mutual_fund_repository: MutualFundRepository):
        self.mutual_fund_repository = mutual_fund_repository
        self.logger = logging.getLogger(__name__)

    def get_all_mutual_funds(self):
        try:
            mutual_funds = self.mutual_fund_repository.get_all_mutual_funds()
            return [self._mutual_fund_to_dto(fund) for fund in mutual_funds]
        except Exception as e:
            self.logger.error(f"Error getting all mutual funds: {str(e)}")
            raise BusinessLogicException(f"Failed to get mutual funds: {str(e)}")

    def get_mutual_fund_by_name(self, fund_name: str):
        try:
            mutual_fund = self.mutual_fund_repository.get_mutual_fund_by_name(fund_name)
            if not mutual_fund:
                raise BusinessLogicException(f"Mutual fund {fund_name} not found")
            return self._mutual_fund_to_dto(mutual_fund)
        except Exception as e:
            self.logger.error(f"Error getting mutual fund {fund_name}: {str(e)}")
            raise BusinessLogicException(f"Failed to get mutual fund: {str(e)}")

    def _mutual_fund_to_dto(self, mutual_fund):
        return {
            'fund_name': mutual_fund.fund_name,
            'category': mutual_fund.category,
            'securities_industry': mutual_fund.securities_industry,
            'fund_type': mutual_fund.fund_type,
            'fund_risk': mutual_fund.fund_risk,
            'dividend_policy': mutual_fund.dividend_policy,
            'redemption_fee': mutual_fund.redemption_fee,
            'purchase_fee': mutual_fund.purchase_fee,
            'fund_expense_ratio': mutual_fund.fund_expense_ratio,
            'minimum_initial_investment': mutual_fund.minimum_initial_investment,
            'fund_registration_date': mutual_fund.fund_registration_date.isoformat(),
            'company': mutual_fund.company,
            'fund_fact': mutual_fund.fund_fact,
            'model_ml_info_path': mutual_fund.model_ml_info_path
        }