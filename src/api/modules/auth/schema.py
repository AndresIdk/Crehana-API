from pydantic import BaseModel, EmailStr, Field


class RegisterUserRequest(BaseModel):
    email: EmailStr = Field(..., example="user@example.com", max_length=255)
    password: str = Field(..., min_length=8, max_length=128, example="mysecurepassword")


class RegisterUserResponse(BaseModel):
    message: str = Field(..., example="User registered successfully")


class LoginUserRequest(BaseModel):
    email: EmailStr = Field(..., example="user@example.com")
    password: str = Field(..., example="mysecurepassword")


class LoginUserResponse(BaseModel):
    message: str = Field(..., example="User logged in successfully")
    token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR...")
