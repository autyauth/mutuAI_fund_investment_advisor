class DatabaseException(Exception):
    def __init__(self, message: str = "A database error occurred", error: Exception = None):
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
class DuplicateEntryException(DatabaseException):
    def __init__(self, message: str = "Duplicate entry found", error: Exception = None):
        super().__init__(message, error)    
class RecordNotFoundException(DatabaseException):
    def __init__(self, message: str = "Record not found", error: Exception = None):
        super().__init__(message, error)


class RecordNotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class DuplicateEntryException(Exception):
    def __init__(self, message: str, original_error: Exception = None):
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)

class DatabaseException(Exception):
    def __init__(self, message: str, original_error: Exception = None):
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)

class InvalidInputException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)