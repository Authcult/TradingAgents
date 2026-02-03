"""
Backend Configuration
"""

import os
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "TradingAgents API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False)
    
    # Server
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    
    # CORS
    CORS_ORIGINS: str = Field(default="http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000,http://127.0.0.1:5173")
    
    # API Keys (从环境变量读取)
    OPENAI_API_KEY: Optional[str] = Field(default=None)
    ALPHA_VANTAGE_API_KEY: Optional[str] = Field(default=None)
    
    # LLM Settings
    LLM_PROVIDER: str = Field(default="modelscope")
    DEEP_THINK_LLM: str = Field(default="Qwen/Qwen2.5-72B-Instruct")
    QUICK_THINK_LLM: str = Field(default="Qwen/Qwen3-235B-A22B-Instruct-2507")
    BACKEND_URL: str = Field(default="https://api-inference.modelscope.cn/v1/")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"
    
    @property
    def cors_origins_list(self) -> list:
        """Parse CORS origins into a list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()
