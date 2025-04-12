from adapters.repositories.nav_history_repository import NavHistoryRepository
from adapters.exceptions import *
from dto.home_reccoment_funds_dto import HomeReccomentFundsDTO
from utils.timeframe_enum import Timeframe
from datetime import datetime, date
import logging
import pandas as pd
import numpy as np
from utils.periods_enum import PeriodsEnum, get_past_date, RocPeriodsEnum, get_roc_past_date
from utils.const import ConstEnum
from adapters.models.performance_mutual_funds_model import PerformanceMutualFundsModel
from adapters.repositories.performance_mutual_funds_repository import PerformanceMutualFundsRepository
from dto.performance_mutual_funds_dto import PerformanceMutualFundsDTO
from pendulum import timezone
from adapters.repositories.mutual_fund_repository import MutualFundRepository
from adapters.repositories.goal_repository import GoalRepository

class PerformanceMutualFundsService:
    def __init__(self, nav_history_repository: NavHistoryRepository, 
                 performance_mutual_funds_repository: PerformanceMutualFundsRepository,
                 mutual_fund_repository: MutualFundRepository,
                 goal_repository: GoalRepository):
        self.nav_history_repository = nav_history_repository
        self.performance_mutual_funds_repository = performance_mutual_funds_repository
        self.mutual_fund_repository = mutual_fund_repository
        self.goal_repository = goal_repository
        
    def create_performance_mutual_funds(self, fund_name:str, date: date):
        nav_histories = self.nav_history_repository.get_nav_history_by_fund_name_and_date_range(
            fund_name,
            get_past_date(PeriodsEnum.ten_year).date(),
            date
        )
        df = pd.DataFrame([{"date": nh.date, "nav": float(nh.nav)} for nh in nav_histories]).sort_values("date")
        df["daily_return"] = df["nav"].pct_change().dropna()
        performance_metrics = {"std": {}, "sharpe_ratio": {}}
        df = df.set_index("date")

        for period in PeriodsEnum:
            if len(df) < period.value:
                continue
            
            df_period = df.loc[get_past_date(period).date():date].copy()
            daily_returns = df_period["daily_return"]
            daily_volatility = daily_returns.std()
            performance_metrics["std"][period.name] = daily_volatility * np.sqrt(252)
            performance_metrics["sharpe_ratio"][period.name] = self._calculate_sharpe_ratio(df_period["nav"].iloc[0],df_period["nav"].iloc[-1], len(df_period), daily_volatility, ConstEnum.risk_free_rate.value)
        performance_data = {}
        for metric, values in performance_metrics.items():
            for period, value in values.items():
                performance_data[f"{metric}_{period}"] = value
        performance_model = PerformanceMutualFundsModel(fund_name=fund_name, date=date, **performance_data)
        self.performance_mutual_funds_repository.create_or_update_performance_mutual_funds(performance_model)
        return performance_metrics

    
    def get_performance_mutual_funds_lastest(self, fund_name: str):
        preformance_model = self.performance_mutual_funds_repository.get_performance_mutual_funds_lastest(fund_name)
        current_roc = self._create_roc_from_today(fund_name, preformance_model.date)
        return PerformanceMutualFundsDTO.from_model(preformance_model, **current_roc).to_dict()
    def get_home_recommend_funds(self):
        funds = [
            HomeReccomentFundsDTO(
                fund_risk=fund.fund_risk,
                **self.get_performance_mutual_funds_lastest(fund.fund_name)
            ).to_dict()
            for fund in self.mutual_fund_repository.get_all_mutual_funds()
        ]

        sorted_funds = sorted(
            funds, 
            key=lambda f: (-int(f["fund_risk"]), -float(f["sharpe_ratio_one_year"]))
        )

        return list(sorted_funds)
    

    def reccoment_funds_with_user_risk_and_rate(self, username: str):
        """
        คัดเลือกกองทุนที่เหมาะสมกับผู้ใช้ โดยใช้ค่าความเสี่ยง (STD) และอัตราผลตอบแทน (ROC)
        เลือกใช้ค่าจากช่วงเวลาที่ยาวที่สุดที่มีข้อมูล และต้องมีอย่างน้อย ROC หรือ STD
        """
        # 🔹 1. ดึงข้อมูลเป้าหมายของผู้ใช้
        year = datetime.now().year
        user_goal = self.goal_repository.get_goal_by_username_and_year(username, year)
        if not user_goal:
            raise ValueError(f"User '{username}' has no investment goal set for {year}")

        target_std = float(user_goal.std_fund) if user_goal.std_fund else 0
        target_roc = float(user_goal.rate_fund) if user_goal.rate_fund else 0

        # 🔹 2. ดึงข้อมูลกองทุนทั้งหมด
        all_funds = self.mutual_fund_repository.get_all_mutual_funds()
        recommended_funds = []

        for fund in all_funds:
            performance = self.performance_mutual_funds_repository.get_performance_mutual_funds_lastest(fund.fund_name)
            if not performance:
                continue  # ถ้าไม่มีข้อมูล performance ให้ข้าม

            # 🔹 3. ค้นหาช่วงเวลาที่ยาวที่สุดที่มีข้อมูลและเข้าเงื่อนไข
            fund_roc = None
            fund_std = None
            selected_period = None
            roc = self._create_roc_from_today(fund.fund_name, performance.date)

            for period in [PeriodsEnum.ten_year, PeriodsEnum.five_year, PeriodsEnum.three_year, PeriodsEnum.one_year]:
                roc_value = roc.get(f"{period.name}_roc")
                std_value = getattr(performance, f"std_{period.name}", None)

                if roc_value is not None or std_value is not None:
                    temp_fund_roc = float(roc_value) if roc_value is not None else None
                    temp_fund_std = float(std_value) if std_value is not None else None

                    # 🔥 **เช็คเงื่อนไขตรงนี้เลย** 🔥
                    if (temp_fund_std <= target_std) and (temp_fund_roc >= target_roc):
                        fund_roc = temp_fund_roc
                        fund_std = temp_fund_std
                        selected_period = period.name
                        break  # ✅ ถ้าเข้าเงื่อนไขแล้ว ออกจากลูป period ทันที

            # 🔹 4. ถ้าเจอช่วงเวลาที่เข้าเงื่อนไขแล้ว ให้นำกองทุนเข้าสู่ลิสต์แนะนำ
            if selected_period:
                recommended_funds.append({
                    "fund_name": fund.fund_name,
                    "fund_risk": fund.fund_risk,
                    "std": round(fund_std*100, 2) if fund_std is not None else None,
                    "roc": round(fund_roc*100,2) if fund_roc is not None else None,
                    "sharpe_ratio": round(float(getattr(performance, f"sharpe_ratio_{selected_period}", 0)),2),  # ค่า Sharpe Ratio 1 ปี
                    "used_period": selected_period  # ระบุช่วงเวลาที่ใช้ข้อมูล
                })

        # 🔹 5. เรียงลำดับกองทุนตาม Sharpe Ratio (มากไปน้อย)
        sorted_funds = sorted(
            recommended_funds,
            key=lambda f: -float(f["fund_risk"]) if f["fund_risk"] is not None else -float("inf")
        )

        return sorted_funds

    # def reccoment_funds_with_user_risk_and_rate(self, username: str):
    #     """
    #     คัดเลือกกองทุนที่เหมาะสมกับผู้ใช้ โดยใช้ค่าความเสี่ยง (STD) และอัตราผลตอบแทน (ROC)
    #     โดยจะเลือกใช้ค่าจากช่วงเวลาที่ยาวที่สุดก่อน ตามลำดับใน PeriodsEnum
    #     """
    #     # 🔹 1. ดึงข้อมูลเป้าหมายของผู้ใช้
    #     year = datetime.now().year
    #     user_goal = self.goal_repository.get_goal_by_username_and_year(username, year)
    #     if not user_goal:
    #         raise ValueError(f"User '{username}' has no investment goal set for {year}")

    #     # ค่าความเสี่ยงและผลตอบแทนที่ผู้ใช้ต้องการ
    #     target_std = float(user_goal.std_fund)
    #     target_roc = float(user_goal.rate_fund)

    #     # 🔹 2. ดึงข้อมูลกองทุนทั้งหมด
    #     all_funds = self.mutual_fund_repository.get_all_mutual_funds()
    #     recommended_funds = []

    #     for fund in all_funds:
    #         # ดึงข้อมูล Performance ของกองทุน
    #         performance = self.performance_mutual_funds_repository.get_performance_mutual_funds_lastest(fund.fund_name)
    #         if not performance:
    #             continue

    #         # 🔹 3. เลือกค่าของ ROC และ STD ตามลำดับความสำคัญจาก PeriodsEnum
    #         fund_roc = None
    #         fund_std = None
    #         selected_period = None  # เก็บชื่อช่วงเวลาที่ใช้
    #         roc = self._create_roc_from_today(fund.fund_name, performance.date)
    #         for period in [PeriodsEnum.ten_year, PeriodsEnum.five_year, PeriodsEnum.three_year, PeriodsEnum.one_year]:
    #             roc_key = f"{period.name}_roc"
    #             std_key = f"std_{period.name}"

    #             # ใช้ getattr() เพื่อดึงค่าจาก object performance
    #             roc_value = float(roc.get(roc_key, None))
    #             std_value = float(getattr(performance, std_key, None))

    #             if roc_value is not None and std_value is not None:
    #                 fund_roc = roc_value
    #                 fund_std = std_value
    #                 selected_period = period.name  # เก็บชื่อช่วงเวลาที่ใช้
    #                 break  # ใช้ค่าที่เจอแรกสุดแล้วออกจากลูป

    #         fund_sharpe = float(getattr(performance, "sharpe_ratio_one_year", None))  # ค่า Sharpe Ratio 1 ปี

    #         if fund_roc is None or fund_std is None:
    #             continue  # ถ้าไม่มีค่าข้อมูลพอ ข้ามไป

    #         # 🔹 4. ตรวจสอบว่ากองทุนอยู่ในช่วงที่เหมาะสมหรือไม่
    #         if (fund_std <= target_std) and (fund_roc >= target_roc ):
    #             recommended_funds.append({
    #                 "fund_name": fund.fund_name,
    #                 "fund_risk": fund.fund_risk,
    #                 "std": fund_std,
    #                 "roc": fund_roc,
    #                 "sharpe_ratio": fund_sharpe,
    #                 "used_period": selected_period  # แจ้งว่าข้อมูลใช้ช่วงเวลาไหน (ten_year, five_year, ฯลฯ)
    #             })

    #     # 🔹 5. เรียงลำดับกองทุนตาม Sharpe Ratio (มากไปน้อย)
    #     sorted_funds = sorted(
    #         recommended_funds, 
    #         key=lambda f: -float(f["sharpe_ratio"]) if f["sharpe_ratio"] is not None else -float("-inf")
    #     )

    #     return sorted_funds



    
    def _create_roc_from_today(self, fund_name: str, end_date: date):
        roc = {}
        today_nav = self.nav_history_repository.get_nav_history_by_fund_name_and_date(fund_name, end_date)
        today_nav_value = float(today_nav.nav)
        for period in RocPeriodsEnum:
            start_date = get_roc_past_date(period, end_date)
            start_nav = self.nav_history_repository.get_nearest_nav_after_date(fund_name, start_date)
            start_nav_value = float(start_nav.nav)
            
            if period.name.endswith("_year") and period.name != "one_year":
                roc[f"{period.name}_roc"] = self._roc(start_nav_value, today_nav_value)**(1/(PeriodsEnum[period.name].value)) - 1
            else:
                roc[f"{period.name}_roc"] = self._roc(start_nav_value, today_nav_value) - 1
        return roc
    
    def _roc(self, start_data, end_data):
        return (float(end_data) / float(start_data))

    def _calculate_sharpe_ratio(self, start_data, end_data, period, daily_volatility, risk_free_rate: float):
        """Calculate the Sharpe ratio for a mutual fund."""
        anualized_return = (end_data / start_data) ** (252 / period) - 1
         
        annualized_volatility = daily_volatility * np.sqrt(252)
        
        if annualized_volatility > 0:
            sharpe_ratio = (anualized_return - risk_free_rate) / annualized_volatility
        else:
            sharpe_ratio = None
        return sharpe_ratio
            
        
        