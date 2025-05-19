from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    API_TOKEN: str

    # class Config:
    #     env_file = ".env"

    db_echo: bool = True

    @property
    def db_conn(self):
        return f"postgresql+asyncpg://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:5432/{self.DB_NAME}"

    @property
    def api_token(self):
        return self.API_TOKEN

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
