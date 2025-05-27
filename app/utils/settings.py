"""
Module. Create pydantic app settings.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


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
