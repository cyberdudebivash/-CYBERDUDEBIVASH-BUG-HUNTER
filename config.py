"""
CYBERDUDEBIVASH - Global Platform Configuration
Path: config.py
Version: 5.0.0 (Hardened)
"""

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # --- Infrastructure ---
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    MAX_CONCURRENT_TASKS: int = 150
    DEFAULT_WORDLIST: str = "wordlists/subdomains_top1000.txt"
    
    # --- Sentinel APEX Integration ---
    # The master key used for both Ingestion and AI Reasoning
    SENTINEL_APEX_KEY: str = os.getenv("SENTINEL_APEX_KEY", "CDB_MASTER_KEY_2026")
    SENTINEL_APEX_URL: str = "https://api.sentinel-apex.com/v1"
    APEX_SECRET_SIGNING_KEY: str = os.getenv("APEX_SIGNING_SECRET", "CDB_HMAC_SECRET")
    
    # --- Platform Modes ---
    GOD_MODE_ENABLED: bool = os.getenv("GOD_MODE_ENABLED", "True").lower() == "true"
    
    class Config:
        env_file = ".env"

settings = Settings()