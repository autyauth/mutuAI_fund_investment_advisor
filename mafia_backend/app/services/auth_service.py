from flask_jwt_extended import create_access_token
import bcrypt
from datetime import timedelta, datetime
from services.exceptions import BusinessLogicException
import logging
from sqlalchemy import text

class AuthService:
    def __init__(self, user_repository):
        self.user_repository = user_repository
        self.logger = logging.getLogger(__name__)

    def authenticate(self, username: str, password: str):
        try:
            self.logger.info(f"Attempting authentication for user: {username}")
            
            user = self.user_repository.get_user(username)
            if not user:
                self.logger.warning(f"User not found: {username}")
                raise BusinessLogicException("Invalid username or password")
            
            # Check password
            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                self.logger.warning(f"Invalid password for user: {username}")
                raise BusinessLogicException("Invalid username or password")

            # Create access token with expiration
            expires = timedelta(hours=1)
            expires_at = datetime.utcnow() + expires
            access_token = create_access_token(
                identity=username,
                expires_delta=expires
            )
            
            # Store token in database
            self.store_token(username, access_token, expires_at)
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "expires_in": 3600  # 1 hour in seconds
            }

        except Exception as e:
            self.logger.error(f"Authentication error: {str(e)}", exc_info=True)
            raise BusinessLogicException(f"Authentication failed: {str(e)}")

    def store_token(self, username: str, token: str, expires_at: datetime):
        session = self.user_repository.database.Session()
        try:
            session.execute(
                text("""
                    INSERT INTO user_tokens (username, token, expires_at)
                    VALUES (:username, :token, :expires_at)
                """),
                {
                    "username": username,
                    "token": token,
                    "expires_at": expires_at
                }
            )
            session.commit()
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error storing token: {str(e)}")
            raise
        finally:
            session.close()

    def register(self, username: str, password: str, email: str, telephone_number: str, birthday: any, job: str = None, salary: float = 0, risk_level: int = 0):
        try:
            # Check if user already exists
            existing_user = self.user_repository.get_user(username)
            if existing_user:
                raise BusinessLogicException("Username already exists")

            # Hash password
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)


            # Create new user with hashed password
            new_user = {
                'username': username,
                'password': hashed_password.decode('utf-8'),  # Store as string
                'email': email,
                'telephone_number': telephone_number,
                'birthday': birthday,
                'job': job,
                'salary': salary,
                'risk_level': risk_level
            }

            self.user_repository.create_user(new_user)
            return {"message": "User registered successfully"}

        except Exception as e:
            self.logger.error(f"Registration error: {str(e)}")
            raise BusinessLogicException(f"Registration failed: {str(e)}")

    