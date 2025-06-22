from .config_base import Settings


class ProductionMysqlSettings(Settings):
    DATABASE_URL: str = "mysql://user:password@localhost:3306/mi_db"
    JWT_SECRET_KEY: str = "secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_TIME: int = 60
    RESEND_API_KEY: str = "re_Gew3VpFJ_ANrJDpfdQvJ4FruGwnuVWPFB"
    RESEND_FROM_EMAIL: str = "support@jaimedev.site"


def get_prod_mysql_settings() -> ProductionMysqlSettings:
    return ProductionMysqlSettings()
