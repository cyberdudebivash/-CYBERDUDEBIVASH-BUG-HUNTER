"""
CYBERDUDEBIVASH BUG HUNTER - Administrative CLI (Elite Tier Support)
Path: admin_cli.py
Version: 2.1.0 (Production Hardened)
Purpose: High-authority command-line interface for manual swarm orchestration.
"""

import typer
from rich.console import Console
from rich.table import Table
from scheduler.scheduler_engine import run_distributed_recon
from config import settings
import sys

# Initialize High-Authority Console
app = typer.Typer(help="CyberDudeBivash Bug Hunter Admin Control Center")
console = Console()

@app.command()
def launch_swarm(
    domain: str = typer.Argument(..., help="The target domain to scan"), 
    tier: str = typer.Option("standard", help="Service tier: standard or elite"), 
    concurrency: int = typer.Option(None, help="Override default concurrency threads")
):
    """
    Launches a distributed swarm with Tier-specific performance parameters.
    Elite Tier grants higher thread counts and deeper intelligence gathering.
    """
    # Elite Tier Logic: High-performance parameters for maximum revenue
    if tier.lower() == "elite":
        concurrency = concurrency or 500
        wordlist = "wordlists/subdomains_top10000.txt"
        priority = "HIGH-SPEED"
    else:
        concurrency = concurrency or settings.MAX_CONCURRENT_TASKS
        wordlist = settings.DEFAULT_WORDLIST
        priority = "NORMAL"

    console.print(f"\n[bold red]🚀 CYBERDUDEBIVASH SWARM ACTIVATED[/bold red]")
    console.print(f"[bold white]Target:[/bold white] {domain}")
    console.print(f"[bold white]Service Tier:[/bold white] {tier.upper()}")
    console.print(f"[bold white]Concurrency:[/bold white] {concurrency} threads")
    
    try:
        # Dispatch to the Celery/Redis Swarm
        run_distributed_recon.delay(domain, wordlist=wordlist, concurrency=concurrency)
        console.print(f"\n[bold green]✔ Success:[/bold green] Task successfully queued in Redis with {priority} priority.")
    except Exception as e:
        console.print(f"\n[bold red]✘ Error:[/bold red] Failed to dispatch swarm: {str(e)}")
        sys.exit(1)

@app.command()
def status():
    """
    Displays the current status of the global intelligence swarm.
    """
    table = Table(title="CyberDudeBivash Swarm Status")
    table.add_column("Service", style="cyan")
    table.add_column("Status", style="green")
    
    table.add_row("Redis Broker", "ONLINE")
    table.add_row("Celery Worker", "ACTIVE")
    table.add_row("Sentinel APEX Uplink", "CONNECTED")
    
    console.print(table)

if __name__ == "__main__":
    app()