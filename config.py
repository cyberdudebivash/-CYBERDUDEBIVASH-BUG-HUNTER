"""
CYBERDUDEBIVASH SENTINEL APEX - Global Configuration
Author: CyberDudeBivash AI Strategic Partner
"""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # --- APP SETTINGS ---
    APP_NAME: str = "CyberDudeBivash Sentinel APEX"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False

    # --- SECURITY ---
    # In production, change this to a long random string
    SECRET_KEY: str = "SUPER_SECRET_BIVASH_KEY_2026_DO_NOT_SHARE"
    ADMIN_API_KEY: str = "BIVASH_CYBER_2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 week

    # --- DATABASE ---
    # Default to SQLite for local dev, overridden by ENV in production
    DATABASE_URL: str = "sqlite+aiosqlite:///./sentinel_apex.db"
    
    # --- REDIS ---
    REDIS_URL: Optional[str] = "redis://localhost:6379/0"

    # --- RECON SETTINGS ---
    MAX_CONCURRENT_TASKS: int = 100
    DEFAULT_WORDLIST: str = "wordlists/subdomains_small.txt"

    # Automatically load from a .env file if it exists
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Initialize settings
settings = Settings()