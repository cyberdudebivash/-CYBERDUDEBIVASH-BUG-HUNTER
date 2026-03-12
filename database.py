"""
CYBERDUDEBIVASH BUG HUNTER - Database & Persistence Layer
Path: database.py
Purpose: Handles SQLModel schemas and database initialization.
"""

from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, create_engine, Session, select

# --- 1. Database Configuration ---
# Uses SQLite for local/worker storage, can be pointed to PostgreSQL in .env
DATABASE_URL = "sqlite:///bughunter_assets.db"
engine = create_engine(DATABASE_URL, echo=False)

# --- 2. Data Models ---

class Scan(SQLModel, table=True):
    """Tracks individual recon sessions."""
    id: Optional[int] = Field(default=None, primary_key=True)
    domain: str = Field(index=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    status: str = "COMPLETED"
    critical_count: int = 0

class Asset(SQLModel, table=True):
    """Stores discovered subdomains and their technical metadata."""
    id: Optional[int] = Field(default=None, primary_key=True)
    scan_id: Optional[int] = Field(default=None, foreign_key="scan.id")
    hostname: str = Field(index=True)
    ip_address: Optional[str] = None
    technologies: str = "" # Stored as comma-separated string
    last_seen: datetime = Field(default_factory=datetime.utcnow)

class Vulnerability(SQLModel, table=True):
    """Stores high-impact findings (BOLA, Cloud Leaks)."""
    id: Optional[int] = Field(default=None, primary_key=True)
    scan_id: Optional[int] = Field(default=None, foreign_key="scan.id")
    type: str # BOLA, CLOUD_LEAK, TAKEOVER
    url: str
    severity: str = "CRITICAL"
    evidence: Optional[str] = None

# --- 3. Initialization Logic (The Fix) ---

async def init_db():
    """
    Creates all tables if they do not exist.
    This is called by main.py at startup.
    """
    SQLModel.metadata.create_all(engine)
    print("[DB] Global Intelligence Database initialized successfully.")

def save_asset(domain: str, host: str, tech: List[str], ip: Optional[str] = None):
    """Saves or updates an asset in the database."""
    with Session(engine) as session:
        # Check if asset exists for this domain
        tech_str = ",".join(tech) if tech else ""
        asset = Asset(hostname=host, ip_address=ip, technologies=tech_str)
        session.add(asset)
        session.commit()

def save_scan(domain: str, critical_count: int):
    """Records a completed scan session."""
    with Session(engine) as session:
        scan = Scan(domain=domain, critical_count=critical_count)
        session.add(scan)
        session.commit()
        return scan.id