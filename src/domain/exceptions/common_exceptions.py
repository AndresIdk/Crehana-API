class DomainException(Exception):
    """Base class for domain exceptions"""


class UserAlreadyExists(DomainException):
    """Exception raised when a user already exists"""

    pass


class UserNotFound(DomainException):
    """Exception raised when a user is not found"""

    pass


class InvalidCredentials(DomainException):
    """Exception raised when invalid credentials are provided"""

    pass


class TaskNotFound(DomainException):
    """Exception raised when a task is not found"""

    pass


class ListTaskNotFound(DomainException):
    """Exception raised when a list task is not found"""

    pass
