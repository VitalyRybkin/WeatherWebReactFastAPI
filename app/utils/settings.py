"""
Module. Create pydantic app settings.
"""

from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent


class DBSettings(BaseModel):
    """
    Class. Database settings.
    """

    db_echo: bool = True
    pool_size: int = 5
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class AuthSettings(BaseModel):
    """
    Class Authentication jwt settings.
    """

    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expires_in: int = 3


class Settings(BaseSettings):
    """
    Class. Create pydantic app settings class
    """

    DB_NAME: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    API_TOKEN: str

    # class Config:
    #     env_file = ".env"

    jwt_authentication: AuthSettings = AuthSettings()
    db_settings: DBSettings = DBSettings()

    @property
    def db_conn(self) -> str:
        """
        Function. app database connection
        :return: app database connection string
        """
        return f"postgresql+asyncpg://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:5432/{self.DB_NAME}"  # pylint: disable=(line-too-long

    @property
    def api_token(self) -> str:
        """
        Function. app api token
        :return: api token
        """
        return self.API_TOKEN

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
