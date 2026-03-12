"""
CYBERDUDEBIVASH BUG HUNTER - Enterprise Command Center
Path: main.py
Version: 10.0.0 (GOD MODE)
Purpose: Primary entry point for local, swarm, and AI-reasoning orchestration.
"""

import asyncio
import sys
import argparse
import logging
from typing import List

# --- Core Platform Component Imports ---
from database import init_db
from pipelines.recon_pipeline import ReconPipeline
from scheduler.scheduler_engine import dispatch_mass_recon
from config import settings

# --- High-Authority Logging Configuration ---
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
    """Enterprise Branding & Global Authority Display."""
    print(r"""
    ==============================================================
     CYBERDUDEBIVASH BUG HUNTER — World-Class AI Recon Platform
    ==============================================================
     GOD MODE: ACTIVE | BOLA | Cloud Swarm | AI-Reasoning Brain
    ==============================================================
    """)

async def run_single_target(domain: str, wordlist: str, god_mode: bool):
    """
    Executes a deep-recon pipeline for a single target.
    In God Mode, findings trigger autonomous attack path expansion.
    """
    logger.info(f"Initiating {'GOD MODE' if god_mode else 'Standard'} scan for: {domain}")
    
    # Update global settings for this runtime
    settings.GOD_MODE_ENABLED = god_mode
    
    pipeline = ReconPipeline(domain=domain, wordlist=wordlist)
    result = await pipeline.run()
    
    if result.get("status") == "SUCCESS":
        logger.info(f"Scan complete. {result.get('critical_count', 0)} Critical findings identified.")
    else:
        logger.error(f"Scan failure for {domain}: {result.get('error', 'Unknown Error')}")

def handle_mass_scan(file_path: str, god_mode: bool):
    """
    Dispatches 1,000+ domains to the distributed Celery swarm.
    God Mode priority ensures these tasks take precedence in the Redis broker.
    """
    try:
        with open(file_path, 'r') as f:
            domains = [line.strip() for line in f if line.strip()]
        
        if not domains:
            logger.warning("Target list is empty. Aborting.")
            return

        settings.GOD_MODE_ENABLED = god_mode
        logger.info(f"Mass Scan Initiated: Dispatching {len(domains)} targets to the swarm...")
        
        # Dispatch with God-Mode Context
        dispatch_mass_recon(domains, god_mode=god_mode)
        print(f"[+] Swarm Activated: {len(domains)} tasks pushed to Redis broker.")
        
    except FileNotFoundError:
        logger.error(f"Target list file not found: {file_path}")
    except Exception as e:
        logger.error(f"Failed to dispatch swarm: {e}")

async def main():
    """Main Orchestration Logic for the CyberDudeBivash Ecosystem."""
    banner()
    
    # 1. Initialize Global Intelligence Database (SQLModel/SQLite)
    await init_db()

    # 2. Argument Parsing for Elite-Tier Operations
    parser = argparse.ArgumentParser(description="CyberDudeBivash Bug Hunter God-Mode CLI")
    parser.add_argument("-d", "--domain", help="Single target domain to scan")
    parser.add_argument("-l", "--list", help="Path to text file for Mass Scan (1,000+ domains)")
    parser.add_argument("-w", "--wordlist", default=settings.DEFAULT_WORDLIST, help="Subdomain wordlist path")
    
    # NEW: God Mode Activation Flag
    parser.add_argument(
        "--god-mode", 
        action="store_true", 
        default=False, 
        help="Enable AI Reasoning Orchestrator and Autonomous Pivoting"
    )

    args = parser.parse_args()

    # 3. Execution Routing
    if args.list:
        handle_mass_scan(args.list, args.god_mode)
    elif args.domain:
        await run_single_target(args.domain, args.wordlist, args.god_mode)
    else:
        parser.print_help()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Core execution interrupted by user.")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"UNHANDLED PLATFORM EXCEPTION: {e}")
        sys.exit(1)