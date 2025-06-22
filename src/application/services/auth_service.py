from datetime import datetime, timedelta

from jose import jwt

from configs import settings
from src.api.modules.auth.schema import LoginUserRequest, RegisterUserRequest
from src.domain.exceptions.common_exceptions import (
    InvalidCredentials,
    UserAlreadyExists,
)
from src.domain.interfaces.auth_interface import IAuthRepository
from src.domain.models.user import User
from src.infrastructure.security.password_hasher import PasswordHasher


class AuthUseCase:
    def __init__(self, repo: IAuthRepository):
        self.repo = repo

    def register_user(self, user: RegisterUserRequest) -> User:
        if self.repo.get_user_by_email(user.email):
            raise UserAlreadyExists(f"User with email {user.email} already exists")

        user_db = User(
            email=user.email,
            hashed_password=PasswordHasher.hash_password(user.password),
        )
        return self.repo.create_user(user_db)

    def login_user(self, user: LoginUserRequest) -> str:
        user_db = self.repo.get_user_by_email(user.email)
        if not user_db or not PasswordHasher.verify_password(
            user.password, user_db.hashed_password
        ):
            raise InvalidCredentials(f"Invalid credentials for user {user.email}")

        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_TIME)
        payload = {"sub": user_db.email, "exp": expire}

        token = jwt.encode(
            payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )

        return token

    def get_user_by_email(self, email: str) -> User:
        return self.repo.get_user_by_email(email)

    def get_user_by_id(self, id_user: int) -> User:
        return self.repo.get_user_by_id(id_user)
