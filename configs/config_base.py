from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRATION_TIME: int
    RESEND_API_KEY: str
    RESEND_FROM_EMAIL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
