from abc import ABC, abstractmethod

from src.domain.models.user import User


class IAuthRepository(ABC):
    @abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> User | None:
        pass
