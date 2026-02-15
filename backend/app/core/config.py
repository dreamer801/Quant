"""
Application configuration settings
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Application
    app_name: str = "Quant Investment Platform"
    debug: bool = True
    version: str = "0.1.0"

    # Database
    database_url: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/quant_platform"

    # Data source
    data_source: str = "akshare"  # akshare or tushare
    tushare_token: Optional[str] = None

    # API settings
    api_prefix: str = "/api"


settings = Settings()
