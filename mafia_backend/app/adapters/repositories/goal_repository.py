from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import List, Optional
from adapters.database.mysql_database import MysqlDatabase
from adapters.models import GoalModel
from adapters.repositories.interfaces.IGoal_repository import IGoalRepository
from services.exceptions import NotFoundException
from adapters.exceptions import *
from sqlalchemy import and_
import logging


class GoalRepository(IGoalRepository):
    def __init__(self, database: MysqlDatabase):
        self.database = database
        self.logger = logging.getLogger(__name__)

    def get_goals_by_username(self, username: str) -> List[GoalModel]:
        """Get all goals for a user"""
        session: Session = self.database.Session()
        try:
            goals = (
                session.query(GoalModel)
                .filter(GoalModel.username == username)
                .order_by(GoalModel.year)
                .all()
            )
            return goals
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving goals: {str(e)}")
            raise DatabaseException("Failed to retrieve goals", e)
        finally:
            session.close()
            
    def get_goal_by_username_and_year(self, username: str, year: int) -> GoalModel:
        session: Session = self.database.Session()
        try:
            goal = (
                session.query(GoalModel)
                .filter(GoalModel.username == username, GoalModel.year == year)
                .first()
            )
            return goal
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving goal: {str(e)}")
            raise DatabaseException("Failed to retrieve goal", e)
        finally:
            session.close()
    
    def get_invested_amount_by_username_and_year(self, username: str, year: int) -> dict:
        session: Session = self.database.Session()
        try:
            goal = (
                session.query(GoalModel)
                .filter(GoalModel.username == username, GoalModel.year == year)
                .first()
            )
            return {
                "rmf_amount_invested": goal.rmf_amount_invested,
                "ssf_amount_invested": goal.ssf_amount_invested,
                "thaiesg_amount_invested": goal.thaiesg_amount_invested
            }
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving invested amount: {str(e)}")
            raise DatabaseException("Failed to retrieve invested amount", e)
        finally:
            session.close()
    
    def create_goal(self, goal: GoalModel) -> None:
        session: Session = self.database.Session()
        try:
            session.add(goal)
            session.commit()
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while creating goal: {str(e)}")
            raise DatabaseException("Failed to create goal", e)
        finally:
            session.close()
    
    def update_user_goal(self, username: str, year: int, goal: int) -> None:
        session: Session = self.database.Session()
        try:
            session.query(GoalModel).filter(GoalModel.username == username, GoalModel.year == year
            ).update({"users_goal": goal})
            session.commit()
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while updating goal: {str(e)}")
            raise DatabaseException("Failed to update goal", e)
        finally:
            session.close()
    def update_invested_amount(
        self, username: str, year: int, 
        rmf_amount_invested: float = None, 
        ssf_amount_invested: float = None, 
        thaiesg_amount_invested: float = None
    ):
        """
        อัปเดตเฉพาะค่าที่กำหนด และทำเป็นการเพิ่ม/ลดค่าโดยใช้ SQL Query เพื่อรองรับหลาย Process พร้อมกัน
        """
        session: Session = self.database.Session()
        try:
            update_data = {}

            if rmf_amount_invested is not None:
                update_data["rmf_amount_invested"] = GoalModel.rmf_amount_invested + rmf_amount_invested
            if ssf_amount_invested is not None:
                update_data["ssf_amount_invested"] = GoalModel.ssf_amount_invested + ssf_amount_invested
            if thaiesg_amount_invested is not None:
                update_data["thaiesg_amount_invested"] = GoalModel.thaiesg_amount_invested + thaiesg_amount_invested

            if not update_data:
                return  # ไม่มีค่าให้ปรับปรุง ไม่ต้องทำอะไร

            result = session.query(GoalModel).filter(
                and_(GoalModel.username == username, GoalModel.year == year)
            ).update(update_data, synchronize_session=False)

            if result == 0:
                raise DatabaseException(f"Goal for user '{username}' in year {year} not found")

            session.commit()
        except SQLAlchemyError as e:
            session.rollback()  # Rollback เมื่อเกิดปัญหา
            self.logger.error(f"Database error while updating invested amount: {str(e)}")
            raise DatabaseException("Failed to update invested amount", e)
        finally:
            session.close()
    

    def get_goal_by_year(self, username: str, year: int) -> Optional[GoalModel]:
        """Get specific goal for a user and year"""
        session: Session = self.database.Session()
        try:
            goal = session.query(GoalModel).filter(
                GoalModel.username == username,
                GoalModel.year == year
            ).first()
            return goal
        except SQLAlchemyError as e:
            self.logger.error(f"Database error while retrieving goal: {str(e)}")
            raise DatabaseException("Failed to retrieve goal", e)
        finally:
            session.close()

    def save_goal(self, goal_data: dict) -> None:
        """
        Save or update goal record
        goal_data should contain: username, year, users_goal (rmf_remaining), and optional fields:
        rate_fund_reccomment, rmf_amount_invested, thaiesg_amount_invested, ssf_amount_invested
        """
        session: Session = self.database.Session()
        try:
            username = goal_data.get('username')
            year = goal_data.get('year')
            rmf_remaining = goal_data.get('users_goal',0)
            
            # rate = goal_data.get('rate_fund',0)
            # std_fund = goal_data.get('std_fund',0)
            # rmf_invested = goal_data.get('rmf_amount_invested', 0)
            # thaiesg_invested = goal_data.get('thaiesg_amount_invested', 0)
            # ssf_invested = goal_data.get('ssf_amount_invested', 0)

            self.logger.info(f"Saving goal record: username={username}, year={year}")
            
            goal = session.query(GoalModel).filter(
                GoalModel.username == username,
                GoalModel.year == year
            ).first()

            if goal:
                goal.users_goal = rmf_remaining
            else:
                goal = GoalModel(
                    username=username,
                    year=year,
                    users_goal=rmf_remaining,
                    rate_fund=0.01,
                    std_fund=0.2,
                    rmf_amount_invested=0,
                    thaiesg_amount_invested=0,
                    ssf_amount_invested=0
                )
                session.add(goal)

            session.commit()
            self.logger.info("Goal record saved successfully")
            
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Database error while saving goal: {str(e)}")
            raise DatabaseException("Failed to save goal", e)
        finally:
            session.close()

    def update_investment_amounts(self, username: str, year: int, fund_type: str, amount: float) -> None:
        """
        Update investment amounts for RMF, Thai ESG, or SSF
        Only tracks buy transactions for tax deduction purposes
        """
        session: Session = self.database.Session()
        try:
            goal = session.query(GoalModel).filter(
                GoalModel.username == username,
                GoalModel.year == year
            ).first()

            if not goal:
                goal = GoalModel(
                    username=username,
                    year=year,
                    users_goal=0,
                    rmf_amount_invested=0,
                    thaiesg_amount_invested=0,
                    ssf_amount_invested=0,
                )
                session.add(goal)

            # Update appropriate amount based on fund type
            if fund_type.upper() == 'RMF':
                current_amount = float(goal.rmf_amount_invested or 0)
                goal.rmf_amount_invested = current_amount + amount
                self.logger.info(f"RMF investment updated: previous={current_amount}, added={amount}, new={goal.rmf_amount_invested}")
            elif fund_type.upper() == 'THAIESG':
                current_amount = float(goal.thaiesg_amount_invested or 0)
                goal.thaiesg_amount_invested = current_amount + amount
                self.logger.info(f"Thai ESG investment updated: previous={current_amount}, added={amount}, new={goal.thaiesg_amount_invested}")
            elif fund_type.upper() == 'SSF':
                current_amount = float(goal.ssf_amount_invested or 0)
                goal.ssf_amount_invested = current_amount + amount
                self.logger.info(f"SSF investment updated: previous={current_amount}, added={amount}, new={goal.ssf_amount_invested}")

            session.commit()
            self.logger.info(f"Investment amount updated for {fund_type} in year {year}")

        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Database error while updating investment amount: {str(e)}")
            raise DatabaseException(f"Failed to update {fund_type} investment amount", e)
        finally:
            session.close()

    def delete_goal(self, username: str, year: int) -> None:
        """Delete a goal record"""
        session: Session = self.database.Session()
        try:
            goal = session.query(GoalModel).filter(
                GoalModel.username == username,
                GoalModel.year == year
            ).first()
            
            if goal:
                session.delete(goal)
                session.commit()
                self.logger.info(f"Goal record deleted for user {username}, year {year}")
            else:
                self.logger.info(f"No goal record found to delete for user {username}, year {year}")
                
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Database error while deleting goal: {str(e)}")
            raise DatabaseException("Failed to delete goal", e)
        finally:
            session.close()

    def update_rate_fund_recommendation(self, username: str, year: int, rate: float) -> None:
        """Update rate fund recommendation for a goal"""
        session: Session = self.database.Session()
        try:
            rate_fund = rate
            session.query(GoalModel).filter(
                GoalModel.username == username,
                GoalModel.year == year
            ).update({"rate_fund": rate_fund})
            session.commit()  
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Database error while updating rate fund recommendation: {str(e)}")
            raise DatabaseException("Failed to update rate fund recommendation", e)
        finally:
            session.close()
    
    def update_std_fund_recommendation(self, username: str, year: int, std_fund: float) -> None:
        """Update standard deviation fund recommendation for a goal"""
        session: Session = self.database.Session()
        try:
            session.query(GoalModel).filter(
                GoalModel.username == username,
                GoalModel.year == year
            ).update({"std_fund": std_fund})
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            self.logger.error(f"Database error while updating standard deviation fund recommendation: {str(e)}")
            raise DatabaseException("Failed to update standard deviation fund recommendation", e)
        finally:
            session.close()