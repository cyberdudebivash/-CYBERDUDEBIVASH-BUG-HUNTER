"""
CYBERDUDEBIVASH BUG HUNTER - Enterprise Command Center
Path: main.py
Version: 5.1.0 (Production Hardened)
"""

import asyncio
import sys
import argparse
import logging
from database import init_db
from pipelines.recon_pipeline import ReconPipeline
from scheduler.scheduler_engine import dispatch_mass_recon

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [CDB-BH-CORE] - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("outputs/logs/production_core.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

async def run_single_target(domain: str, wordlist: str):
    """Executes a deep-recon pipeline for a single target."""
    logger.info(f"Starting localized scan for target: {domain}")
    pipeline = ReconPipeline(domain=domain, wordlist=wordlist)
    result = await pipeline.run()
    
    if result.get("status") == "SUCCESS":
        logger.info(f"Scan complete. {result.get('critical_count', 0)} Critical findings identified.")
    else:
        logger.error(f"Scan failed: {result.get('error')}")

def handle_mass_scan(file_path: str):
    """Dispatches targets to the distributed Celery swarm."""
    try:
        with open(file_path, 'r') as f:
            domains = [line.strip() for line in f if line.strip()]
        
        logger.info(f"Mass Scan Initiated: Dispatching {len(domains)} targets to the swarm...")
        dispatch_mass_recon(domains)
        print(f"[+] Swarm Activated: {len(domains)} tasks pushed to Redis broker.")
    except Exception as e:
        logger.error(f"Failed to load target list: {e}")

async def main():
    await init_db()
    parser = argparse.ArgumentParser(description="CyberDudeBivash Bug Hunter CLI")
    parser.add_argument("-d", "--domain", help="Single target domain to scan")
    parser.add_argument("-l", "--list", help="Path to text file for Mass Scan")
    parser.add_argument("-w", "--wordlist", default="wordlists/subdomains_top1000.txt", help="Wordlist path")
    parser.add_argument("--mode", choices=['local', 'swarm'], default='local', help="Execution mode")

    args = parser.parse_args()

    if args.list:
        handle_mass_scan(args.list)
    elif args.domain:
        await run_single_target(args.domain, args.wordlist)
    else:
        parser.print_help()

if __name__ == "__main__":
    asyncio.run(main())