from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    environment: str
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )


settings = Settings()