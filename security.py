import secrets
import hashlib
from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    hashed_api_key: str = Field(index=True)
    tier: str = "free"  # free, pro, enterprise

def generate_api_key() -> str:
    """Generate a high-entropy API key."""
    return f"cb_{secrets.token_urlsafe(32)}"

def hash_key(key: str) -> str:
    """Hash the key for secure DB storage (one-way)."""
    return hashlib.sha256(key.encode()).hexdigest()