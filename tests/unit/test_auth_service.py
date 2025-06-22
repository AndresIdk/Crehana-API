from unittest.mock import MagicMock, patch

import pytest

from src.api.modules.auth.schema import LoginUserRequest, RegisterUserRequest
from src.application.services.auth_service import AuthUseCase
from src.domain.exceptions.common_exceptions import (
    InvalidCredentials,
    UserAlreadyExists,
)


class TestAuthUseCase:
    @pytest.fixture
    def auth_service(self):
        mock_repo = MagicMock()
        return AuthUseCase(mock_repo)

    @pytest.fixture
    def register_request(self):
        return RegisterUserRequest(email="test@example.com", password="password123")

    @pytest.fixture
    def login_request(self):
        return LoginUserRequest(email="test@example.com", password="password123")

    def test_register_user_success(self, auth_service, register_request):
        mock_user = MagicMock()
        mock_user.email = "test@example.com"
        auth_service.repo.get_user_by_email.return_value = None
        auth_service.repo.create_user.return_value = mock_user

        result = auth_service.register_user(register_request)

        assert result == mock_user
        auth_service.repo.get_user_by_email.assert_called_once_with(
            register_request.email
        )

    def test_register_user_already_exists(self, auth_service, register_request):
        mock_user = MagicMock()
        auth_service.repo.get_user_by_email.return_value = mock_user

        with pytest.raises(UserAlreadyExists):
            auth_service.register_user(register_request)

    def test_login_user_success(self, auth_service, login_request):
        mock_user = MagicMock()
        mock_user.email = "test@example.com"
        mock_user.hashed_password = "hashed_password"
        auth_service.repo.get_user_by_email.return_value = mock_user

        with patch(
            "src.infrastructure.security.password_hasher.PasswordHasher.verify_password",
            return_value=True,
        ):
            with patch("jose.jwt.encode", return_value="fake_token"):
                result = auth_service.login_user(login_request)

                assert result == "fake_token"

    def test_login_user_not_found(self, auth_service, login_request):
        auth_service.repo.get_user_by_email.return_value = None

        with pytest.raises(InvalidCredentials):
            auth_service.login_user(login_request)

    def test_login_user_invalid_password(self, auth_service, login_request):
        mock_user = MagicMock()
        mock_user.email = "test@example.com"
        mock_user.hashed_password = "hashed_password"
        auth_service.repo.get_user_by_email.return_value = mock_user

        with patch(
            "src.infrastructure.security.password_hasher.PasswordHasher.verify_password",
            return_value=False,
        ):
            with pytest.raises(InvalidCredentials):
                auth_service.login_user(login_request)

    def test_get_user_by_email(self, auth_service):
        mock_user = MagicMock()
        email = "test@example.com"
        auth_service.repo.get_user_by_email.return_value = mock_user

        result = auth_service.get_user_by_email(email)

        assert result == mock_user
        auth_service.repo.get_user_by_email.assert_called_once_with(email)

    def test_get_user_by_id(self, auth_service):
        mock_user = MagicMock()
        user_id = 1
        auth_service.repo.get_user_by_id.return_value = mock_user

        result = auth_service.get_user_by_id(user_id)

        assert result == mock_user
        auth_service.repo.get_user_by_id.assert_called_once_with(user_id)
