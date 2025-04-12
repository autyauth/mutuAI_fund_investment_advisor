from services.exceptions import BusinessLogicException
from adapters.repositories.goal_repository import GoalRepository
from datetime import datetime
class GoalService:
    def __init__(self, goal_repository: GoalRepository):
        self.goal_repository = goal_repository

    def get_goals_by_username(self, username: str):
        goals = self.goal_repository.get_goals_by_username(username)
        if not goals:
            return []
        return [self._goal_to_dto(g) for g in goals]
    def get_goal_by_username_and_year(self, username: str, year: int):
        goal = self.goal_repository.get_goal_by_username_and_year(username, year)
        if not goal:
            return None
        return self._goal_to_dto(goal)
        
    
    def update_rate(self, data: dict):
        username = data['username']
        rate_fund = data['rate_fund']
        year = datetime.now().year
        self.goal_repository.update_rate_fund_recommendation(username,year, rate_fund)
    
    def update_std(self, data: dict):
        username = data['username']
        std_fund = data['std_fund']
        year = datetime.now().year
        self.goal_repository.update_std_fund_recommendation(username,year, std_fund)
        

    def _goal_to_dto(self, goal):
        return {
            'year': goal.year,
            'users_goal': float(goal.users_goal) if goal.users_goal else 0,
            'rate_fund': float(goal.rate_fund) if goal.rate_fund else 0,
            'std_fund': float(goal.std_fund) if goal.std_fund else 0,
            'rmf_amount_invested': float(goal.rmf_amount_invested) if goal.rmf_amount_invested else 0,
            'ssf_amount_invested': float(goal.ssf_amount_invested) if goal.ssf_amount_invested else 0,
            'thaiesg_amount_invested': float(goal.thaiesg_amount_invested) if goal.thaiesg_amount_invested else 0,
        }