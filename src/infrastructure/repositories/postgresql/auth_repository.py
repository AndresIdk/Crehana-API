from sqlalchemy.orm import Session

from src.domain.interfaces.auth_interface import IAuthRepository
from src.domain.models.user import User


class AuthRepositoryPostgres(IAuthRepository):
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: User) -> User:
        user.save(self.db)
        return user

    def get_user_by_email(self, email: str) -> User:
        return User.get_by_email(self.db, email)

    def get_user_by_id(self, id_user: int) -> User:
        return User.get_by_id(self.db, id_user)
