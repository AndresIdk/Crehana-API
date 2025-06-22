from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies.DI import get_auth_repository_postgres
from src.api.modules.auth.schema import (
    LoginUserRequest,
    LoginUserResponse,
    RegisterUserRequest,
    RegisterUserResponse,
)
from src.application.services.auth_service import AuthUseCase
from src.domain.exceptions.common_exceptions import (
    InvalidCredentials,
    UserAlreadyExists,
)
from src.domain.interfaces.auth_interface import IAuthRepository

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register", response_model=RegisterUserResponse, tags=["Auth"])
def register_user(
    request: RegisterUserRequest,
    repo: IAuthRepository = Depends(get_auth_repository_postgres),
):
    usecase = AuthUseCase(repo)
    try:
        user = usecase.register_user(request)
        return RegisterUserResponse(
            message=f"User {user.email} registered successfully"
        )
    except UserAlreadyExists as e:
        raise HTTPException(status_code=400, detail=str(e))


@auth_router.post("/login", response_model=LoginUserResponse, tags=["Auth"])
def login_user(
    request: LoginUserRequest,
    repo: IAuthRepository = Depends(get_auth_repository_postgres),
):
    usecase = AuthUseCase(repo)
    try:
        token = usecase.login_user(request)
        return LoginUserResponse(message="User logged in successfully", token=token)
    except InvalidCredentials as e:
        raise HTTPException(status_code=401, detail=str(e))
