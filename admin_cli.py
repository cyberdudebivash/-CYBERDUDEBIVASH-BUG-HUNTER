"""
CYBERDUDEBIVASH SENTINEL APEX - Admin Control Panel
Usage: python admin_cli.py create-user "JohnDoe" --tier pro
"""

import typer
import asyncio
import secrets
import hashlib
from sqlmodel import Session, select
from database import engine, User, init_db # Import from our existing database.py

app = typer.Typer(help="CyberDudeBivash Sentinel APEX Administrative Tool")

def generate_secure_key() -> str:
    """Creates a high-entropy key: cb_ + 32 random chars."""
    return f"cb_{secrets.token_urlsafe(32)}"

def hash_api_key(key: str) -> str:
    """One-way hash for secure storage."""
    return hashlib.sha256(key.encode()).hexdigest()

@app.command()
def create_user(
    username: str = typer.Argument(..., help="The unique name for the user/client"),
    tier: str = typer.Option("free", help="Access tier: free, pro, or enterprise")
):
    """Register a new user and generate their unique API key."""
    raw_key = generate_secure_key()
    hashed = hash_api_key(raw_key)

    with Session(engine) as session:
        # Check if user exists
        existing = session.exec(select(User).where(User.username == username)).first()
        if existing:
            typer.secho(f"Error: User '{username}' already exists.", fg=typer.colors.RED)
            raise typer.Exit()

        new_user = User(username=username, hashed_key=hashed, tier=tier)
        session.add(new_user)
        session.commit()

    typer.secho(f"✅ User '{username}' created successfully!", fg=typer.colors.GREEN, bold=True)
    typer.echo(f"Tier: {tier.upper()}")
    typer.secho(f"API Key: {raw_key}", fg=typer.colors.CYAN, bold=True)
    typer.echo("⚠️  SAVE THIS KEY. It will not be shown again.")

@app.command()
def list_users():
    """Display all registered users and their tiers."""
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        if not users:
            typer.echo("No users found in the database.")
            return
        
        for user in users:
            typer.echo(f"ID: {user.id} | User: {user.username} | Tier: {user.tier.upper()}")

@app.command()
def update_tier(username: str, tier: str):
    """Upgrade or downgrade a user's subscription tier."""
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == username)).first()
        if not user:
            typer.secho(f"User '{username}' not found.", fg=typer.colors.RED)
            return
        
        user.tier = tier
        session.add(user)
        session.commit()
        typer.echo(f"Success: '{username}' is now on the {tier.upper()} tier.")

if __name__ == "__main__":
    app()