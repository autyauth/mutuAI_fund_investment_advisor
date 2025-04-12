import bcrypt
from datetime import date
from services.exceptions import BusinessLogicException
from adapters.models import UserModel
import logging

class UserManagementService:
    def __init__(self, user_repository):
        self.user_repository = user_repository
        self.logger = logging.getLogger(__name__)

    def create_user(self, username: str, password: str, email: str, telephone_number: str, birthday: any):
        try:
            # Hash password
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            
            # Create user with hashed password
            user = UserModel(
                username=username,
                password=hashed_password.decode('utf-8'),  # Store as string
                email=email,
                telephone_number=telephone_number,
                birthday=birthday,
                risk_level=0,  
            )
            
            self.user_repository.create_user(user)
            return {"message": "User created successfully"}
            
        except Exception as e:
            self.logger.error(f"Error creating user: {str(e)}")
            raise BusinessLogicException(f"Failed to create user: {str(e)}")

    def update_password(self, username: str, old_password: str, new_password: str):
        try:
            user = self.user_repository.get_user(username)
            if not user:
                raise BusinessLogicException("User not found")

            # Verify old password
            if not bcrypt.checkpw(old_password.encode('utf-8'), user.password.encode('utf-8')):
                raise BusinessLogicException("Invalid password")

            # Hash new password
            salt = bcrypt.gensalt()
            new_hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), salt)
            
            # Update password
            user.password = new_hashed_password.decode('utf-8')
            self.user_repository.update_user(user)
            
            return {"message": "Password updated successfully"}
            
        except Exception as e:
            self.logger.error(f"Error updating password: {str(e)}")
            raise BusinessLogicException(f"Failed to update password: {str(e)}")