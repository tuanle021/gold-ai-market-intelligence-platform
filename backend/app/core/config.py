from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    environment: str
    debug: bool = False
    market_provider: str = "mock"

    twelve_data_api_key: str | None = None
    twelve_data_base_url: str = "https://api.twelvedata.com"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )


settings = Settings()