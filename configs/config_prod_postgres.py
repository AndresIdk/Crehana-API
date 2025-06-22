from .config_base import Settings


class ProductionPostgresSettings(Settings):
    DATABASE_URL: str = (
        "postgresql+psycopg2://crehana_user:crehana_password@postgres:5432/task_manager"
    )
    JWT_SECRET_KEY: str = "secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_TIME: int = 60
    RESEND_API_KEY: str = "re_Gew3VpFJ_ANrJDpfdQvJ4FruGwnuVWPFB"
    RESEND_FROM_EMAIL: str = "support@jaimedev.site"


def get_prod_postgres_settings() -> ProductionPostgresSettings:
    return ProductionPostgresSettings()
