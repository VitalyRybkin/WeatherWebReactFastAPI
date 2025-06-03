"""
Module. Create pydantic app settings.
"""

from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent


class AuthSettings(BaseModel):
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

    db_echo: bool = True

    jwt_authentication: AuthSettings = AuthSettings()

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
