class NotFoundException(Exception):
    def __init__(self, message: str = "Not found", error: Exception = None):
        self.message = message
        self.error = error

    def __str__(self) -> str:
        return self.message

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "message": self.message,
            "details": str(self.error) if self.error else None
        }

class InternalErrorException(Exception):
    def __init__(self, message: str = "Internal error occurred", error: Exception = None):
        self.message = message
        self.error = error

    def __str__(self) -> str:
        return self.message

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "message": self.message,
            "details": str(self.error) if self.error else None
       }

class InvalidInputException(Exception):
    def __init__(self, message: str = "Invalid Input parameter", error: Exception = None):
        self.message = message
        self.error = error

    def __str__(self) -> str:
        return self.message

    def to_dict(self):
        return {
            "type": self.__class__.__name__,
            "message": self.message,
            "details": str(self.error) if self.error else None
        }
    

class BusinessLogicException(Exception):
    """Exception raised when business logic validation fails"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'Business Logic Error: {self.message}'

class DatabaseException(Exception):
    """Exception raised when database operations fail"""
    def __init__(self, message: str, original_error: Exception = None):
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)

    def __str__(self):
        if self.original_error:
            return f'Database Error: {self.message} - Original error: {str(self.original_error)}'
        return f'Database Error: {self.message}'
    
class UserNotFoundException(NotFoundException):
    def __init__(self, message: str = "User not found", error: Exception = None):
        super().__init__(message, error)

class ValidationError(InvalidInputException):
    def __init__(self, message: str = "Validation error", error: Exception = None):
        super().__init__(message, error)