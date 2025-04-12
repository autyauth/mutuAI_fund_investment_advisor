from adapters.repositories.prediction_trend_funds_repository import PredictionTrendFundsRepository

from adapters.repositories.goal_repository import GoalRepository

from adapters.repositories.portfolio_repository import PortfolioRepository
from adapters.repositories.deduction_2025_repository import Deduction2025Repository
from adapters.repositories.deduction_repository import DeductionRepository

from dto.user_advise_dto import UserAdviseDTO
from utils.advise_enum import AdviseEnum

from datetime import datetime

from services.exceptions import NotFoundException

from adapters.exceptions import RecordNotFoundException




class AdvisorService:
    def __init__(self, prediction_trend_funds_repository: PredictionTrendFundsRepository, goal_repository: GoalRepository, portfolio_repository: PortfolioRepository,
                 deduction_2025_repository: Deduction2025Repository, deduction_repository: DeductionRepository):
        self.prediction_trend_funds_repository = prediction_trend_funds_repository
        self.goal_repository = goal_repository
        self.portfolio_repository = portfolio_repository
        self.deduction_2025_repository = deduction_2025_repository
        self.deduction_repository = deduction_repository
    
    def analyze_and_advise_user_funds(self, username: str, current_date: datetime):
        """
        วิเคราะห์ข้อมูลการลงทุนของผู้ใช้ และให้คำแนะนำ (BUY / HOLD)
        """
        user_advise_dto = UserAdviseDTO(username, current_date.strftime("%Y-%m-%d"), None, [], [], 0, 0)
        user_goal = self.goal_repository.get_goal_by_username_and_year(username, current_date.year)
        
        if user_goal is None:
            raise NotFoundException(f"Goal not found for user {username}")
        funds = self.portfolio_repository.get_funds_from_portfolio_by_username_holding_units(username)
        
        # วิเคราะห์ว่าควรซื้อเพิ่มหรือไม่
        total_invested = user_goal.rmf_amount_invested if user_goal.rmf_amount_invested else 0
        
        ### ไม่ใช้แล้วเพราะว่า goal สร้างจาก rmf ที่เหลือที่ต้องลงทุน
        # total_invested += user_goal.ssf_amount_invested if user_goal.ssf_amount_invested and current_date.year < 2025 else 0
        # total_invested += user_goal.thaiesg_amount_invested if user_goal.thaiesg_amount_invested else 0
        
        # if current_date.year >= 2025:
        #     total_invested += self.deduction_2025_repository.get_sum_rmf_thaiesg_deduction(username, current_date.year)
        # else:
        #     total_invested += self.deduction_repository.get_sum_rmf_ssf_thaiesg_deduction(username, current_date.year)

        remainingInvestmentNeeded = user_goal.users_goal * current_date.month / 12
        user_advise_dto.remain_amount_month = max(round(remainingInvestmentNeeded - total_invested, 2), 0)
        user_advise_dto.remain_amount_year = max(round(user_goal.users_goal - total_invested, 2), 0)

        is_decem_month = current_date.month == 12

        # ตรวจสอบว่าการลงทุนถึงเป้าหมายหรือไม่
        if total_invested < remainingInvestmentNeeded:
            user_advise_dto.remainingInvestmentNeeded = AdviseEnum.UNFULL_BALANCE_YEAR if is_decem_month else AdviseEnum.UNFULL_BALANCE_MONTH
        else:
            user_advise_dto.remainingInvestmentNeeded = AdviseEnum.FULL_BALANCE_YEAR if is_decem_month else AdviseEnum.FULL_BALANCE_MONTH

        # วิเคราะห์แนวโน้มและให้คำแนะนำ
        for fund in funds:
            try:
                pred_trend_fund = self.prediction_trend_funds_repository.get_prediction_trend_funds_lastest(fund)
            except RecordNotFoundException as e:
                continue


            is_trend_up = pred_trend_fund.trend == 1
            investment_status = user_advise_dto.remainingInvestmentNeeded  # ตรวจสอบสถานะการลงทุน
            if is_trend_up:
                user_advise_dto.trend_up_funds.append(fund)
            else:
                user_advise_dto.non_trend_up_funds.append(fund)

            # **กำหนดคำแนะนำ BUY / HOLD**
            if is_trend_up and (investment_status == AdviseEnum.UNFULL_BALANCE_MONTH or investment_status == AdviseEnum.UNFULL_BALANCE_YEAR):
                user_advise_dto.advise_funds.append((fund, "BUY"))
            elif is_trend_up and investment_status == AdviseEnum.FULL_BALANCE_YEAR:
                user_advise_dto.advise_funds.append((fund, "HOLD"))
            elif not is_trend_up:
                user_advise_dto.advise_funds.append((fund, "HOLD"))

        return user_advise_dto.to_dict()
