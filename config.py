"""
CYBERDUDEBIVASH SENTINEL APEX - Global Configuration
Author: CyberDudeBivash AI Strategic Partner
Path: config.py
"""

import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # --- APP SETTINGS ---
    APP_NAME: str = "CyberDudeBivash Sentinel APEX"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False

    # --- SECURITY HARDENING ---
    # These MUST be set in the .env file for production security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "SUPER_SECRET_BIVASH_KEY_PROD_2026")
    ADMIN_API_KEY: str = os.getenv("ADMIN_API_KEY", "BIVASH_CYBER_PLATFORM_KEY")
    SENTINEL_APEX_KEY: str = os.getenv("SENTINEL_APEX_KEY", "")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 1 week

    # --- DATABASE & PERSISTENCE ---
    DATABASE_URL: str = "sqlite+aiosqlite:///./bughunter_assets.db"
    
    # --- REDIS & CELERY ---
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # --- RECON PARAMETERS ---
    MAX_CONCURRENT_TASKS: int = 200
    DEFAULT_WORDLIST: str = "wordlists/subdomains_top1000.txt"

    # Automatically load from a .env file if it exists
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Initialize global singleton settings
settings = Settings()