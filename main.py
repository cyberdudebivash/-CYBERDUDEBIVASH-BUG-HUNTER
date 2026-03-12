"""
CYBERDUDEBIVASH BUG HUNTER - Enterprise Command Center
Path: main.py
Version: 5.0.0 (Production Hardened)

The primary entry point for the world-class Bug Hunter platform.
Supports local execution, distributed swarm dispatching, and real-time monitoring.
"""

import asyncio
import sys
import argparse
import logging
from typing import List

# Core Platform Imports
from config import settings
from pipelines.recon_pipeline import ReconPipeline
from scheduler.scheduler_engine import dispatch_mass_recon
from database import init_db

# Configure high-authority logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [CDB-BH-CORE] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("outputs/logs/production_core.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def banner():
    """Enterprise Branding & Authority."""
    print(r"""
    ==============================================================
     CYBERDUDEBIVASH BUG HUNTER — World-Class AI Recon Platform
    ==============================================================
     BOLA | Cloud Leaks | Distributed Swarm | Real-Time Alerts
    ==============================================================
    """)

async def run_single_target(domain: str, wordlist: str):
    """Executes a deep-recon pipeline for a single target (Dev/Debug Mode)."""
    logger.info(f"Starting localized scan for target: {domain}")
    pipeline = ReconPipeline(domain=domain, wordlist=wordlist)
    result = await pipeline.run()
    
    if result["status"] == "SUCCESS":
        logger.info(f"Scan complete. {result['critical_count']} Critical findings identified.")
    else:
        logger.error(f"Scan failed: {result.get('error')}")

def handle_mass_scan(file_path: str):
    """Dispatches 1,000+ domains to the distributed Celery swarm."""
    try:
        with open(file_path, 'r') as f:
            domains = [line.strip() for line in f if line.strip()]
        
        logger.info(f"Mass Scan Initiated: Dispatching {len(domains)} targets to the swarm...")
        dispatch_mass_recon(domains)
        print(f"[+] Swarm Activated: {len(domains)} tasks pushed to Redis broker.")
    except Exception as e:
        logger.error(f"Failed to load target list: {e}")

async def main():
    banner()
    
    # Initialize the Global Intelligence Database
    await init_db()

    parser = argparse.ArgumentParser(description="CyberDudeBivash Bug Hunter CLI")
    parser.add_argument("-d", "--domain", help="Single target domain to scan")
    parser.add_argument("-l", "--list", help="Path to text file containing multiple domains for Mass Scan")
    parser.add_argument("-w", "--wordlist", default="wordlists/subdomains_top1000.txt", help="Path to subdomain wordlist")
    parser.add_argument("--mode", choices=['local', 'swarm'], default='local', help="Execution mode")

    args = parser.parse_args()

    if args.list:
        # Trigger Distributed Swarm Logic (Highest Max Profit)
        handle_mass_scan(args.list)
    elif args.domain:
        # Trigger Localized Recon Pipeline
        await run_single_target(args.domain, args.wordlist)
    else:
        parser.print_help()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Core execution interrupted by user.")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Unhandled Platform Exception: {e}")
        sys.exit(1)