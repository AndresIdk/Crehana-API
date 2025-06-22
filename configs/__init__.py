import os

from .config_base import Settings
from .config_dev_mysql import get_dev_mysql_settings
from .config_dev_postgres import get_dev_postgres_settings
from .config_prod_mysql import get_prod_mysql_settings
from .config_prod_postgres import get_prod_postgres_settings


def get_config() -> Settings:
    environment = os.getenv("APP_SETTINGS_MODULE")

    if environment == "prod_postgres":
        return get_prod_postgres_settings()
    elif environment == "dev_postgres":
        return get_dev_postgres_settings()
    elif environment == "prod_mysql":
        return get_prod_mysql_settings()
    elif environment == "dev_mysql":
        return get_dev_mysql_settings()
    else:
        return get_dev_postgres_settings()


settings = get_config()
