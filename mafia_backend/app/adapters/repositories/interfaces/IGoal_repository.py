from abc import ABC, abstractmethod
from adapters.models import GoalModel

class IGoalRepository(ABC):
    @abstractmethod
    def get_goals_by_username(self, username: str) -> list[GoalModel]:
        pass