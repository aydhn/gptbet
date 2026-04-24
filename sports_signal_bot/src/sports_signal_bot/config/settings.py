from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional

class AppSettings(BaseSettings):
    app_name: str = "SportsSignalBot"
    environment: str = "dev"
    debug: bool = False

    model_config = SettingsConfigDict(env_prefix="APP_", env_file=".env", extra="ignore")

class DataSettings(BaseSettings):
    raw_dir: str = "data/raw"
    processed_dir: str = "data/processed"

    model_config = SettingsConfigDict(env_prefix="DATA_", env_file=".env", extra="ignore")

class NotificationSettings(BaseSettings):
    telegram_bot_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None

    model_config = SettingsConfigDict(env_prefix="NOTIFY_", env_file=".env", extra="ignore")

class ModelSettings(BaseSettings):
    baseline_threshold: float = 0.5

    model_config = SettingsConfigDict(env_prefix="MODEL_", env_file=".env", extra="ignore")

class ExperimentSettings(BaseSettings):
    experiment_name: str = "smoke"
    run_id: str = "001"

    model_config = SettingsConfigDict(env_prefix="EXP_", env_file=".env", extra="ignore")

class Settings(BaseSettings):
    app: AppSettings = Field(default_factory=AppSettings)
    data: DataSettings = Field(default_factory=DataSettings)
    notify: NotificationSettings = Field(default_factory=NotificationSettings)
    model: ModelSettings = Field(default_factory=ModelSettings)
    experiment: ExperimentSettings = Field(default_factory=ExperimentSettings)

def get_settings() -> Settings:
    return Settings()
