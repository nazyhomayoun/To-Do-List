class TodoBaseException(Exception):
    """Base exception for all todo application exceptions"""
    
    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)
    
    def __str__(self):
        if self.details:
            return f"{self.message} | Details: {self.details}"
        return self.message


class RepositoryException(TodoBaseException):
    """Base exception for repository layer"""
    pass


class ServiceException(TodoBaseException):
    """Base exception for service layer"""
    pass


class ValidationException(ServiceException):
    """Exception for validation errors"""
    pass


class NotFoundException(RepositoryException):
    """Exception when entity is not found"""
    pass


class DuplicateException(RepositoryException):
    """Exception when duplicate entity is found"""
    pass


class DatabaseException(RepositoryException):
    """Exception for database errors"""
    pass
