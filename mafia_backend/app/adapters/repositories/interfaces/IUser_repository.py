from abc import ABC, abstractmethod
from adapters.models import UserModel
from typing import Optional

class IUserRepository(ABC):
    @abstractmethod
    def get_user(self, username: str) -> Optional[UserModel]:
        """Get user by username"""
        pass

    @abstractmethod
    def create_user(self, user_data: dict) -> None:
        """Create a new user"""
        pass

    @abstractmethod
    def update(self, user_data: dict, username: str) -> UserModel:
        """Update user information"""
        pass

    @abstractmethod
    def get_by_username(self, username: str) -> Optional[UserModel]:
        """Get user by username (for auth)"""
        pass
