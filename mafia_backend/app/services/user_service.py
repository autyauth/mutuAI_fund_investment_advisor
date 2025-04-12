from services.exceptions import BusinessLogicException, UserNotFoundException, ValidationError
from adapters.repositories.user_repository import UserRepository
from datetime import datetime
import re

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user_by_username(self, username: str):
        user = self.user_repository.get_user(username)
        if not user:
            raise UserNotFoundException(f"User {username} not found")
        return self._user_to_dto(user)
    
    def update_user_risk_level(self, username: str, risk_level: int):
        """Update user risk level"""
        if risk_level < 1 or risk_level > 5:
            raise BusinessLogicException("Risk level must be between 1 and 5")
        
        user = self.user_repository.get_user(username)
        if not user:
            raise UserNotFoundException(f"User {username} not found")
        
        updated_user = self.user_repository.update_risk_level(username, risk_level)
        return updated_user
    
    def update_user_info(self, username: str, update_data: dict):
        """Update user information"""
        # First check if user exists
        user = self.user_repository.get_user(username)
        if not user:
            raise UserNotFoundException(f"User {username} not found")
        
        # Validate input data
        if 'email' in update_data:
            self._validate_email(update_data['email'])
            
        if 'telephone_number' in update_data:
            self._validate_phone(update_data['telephone_number'])
            
        if 'birthday' in update_data:
            try:
                # Convert string to date object
                birthday = datetime.strptime(update_data['birthday'], '%Y-%m-%d').date()
                update_data['birthday'] = birthday
            except ValueError:
                raise ValidationError("Invalid birthday format. Use YYYY-MM-DD")
            
        if 'job' in update_data:
            if not update_data['job'] or len(update_data['job']) > 100:
                raise ValidationError("Job must be between 1 and 100 characters")
        
        # Update user in repository
        updated_user = self.user_repository.update(update_data, username)
        return updated_user

    def _validate_email(self, email: str):
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(email):
            raise ValidationError("Invalid email format")

    def _validate_phone(self, phone: str):
        # Adjust pattern based on your specific phone number format requirements
        phone_pattern = re.compile(r'^\+?1?\d{9,15}$')
        if not phone_pattern.match(phone):
            raise ValidationError("Invalid phone number format")

    def _user_to_dto(self, user):
        return {
            'username': user.username,
            'email': user.email,
            'telephone_number': user.telephone_number,
            'birthday': user.birthday.isoformat() if user.birthday else None,
            'job': user.job,
            'salary': float(user.salary) if user.salary else None,
            'risk_level': user.risk_level,
        }