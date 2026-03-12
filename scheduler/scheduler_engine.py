"""
CYBERDUDEBIVASH BUG HUNTER - Distributed Scheduler Engine
Path: scheduler/scheduler_engine.py
Architecture: Celery + Redis + Asyncio
"""

import asyncio
import logging
from celery import Celery
from config import settings

# --- 1. Initialize Celery Swarm Core ---
celery_app = Celery(
    "cyberdude_swarm",
    broker=settings.REDIS_URL,
    backend="redis://localhost:6379/1"
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    broker_connection_retry_on_startup=True
)

@celery_app.task(name="tasks.run_distributed_recon", bind=True, max_retries=3)
def run_distributed_recon(self, domain: str, wordlist: str = None, concurrency: int = None):
    """
    The Swarm Task: Uses local import to break circular dependency.
    """
    # FIX: Local import prevents circular dependency with reasoning_orchestrator
    from pipelines.recon_pipeline import ReconPipeline
    
    if wordlist is None:
        wordlist = settings.DEFAULT_WORDLIST
    
    actual_concurrency = concurrency or settings.MAX_CONCURRENT_TASKS

    print(f"[SWARM-NODE] Received Target: {domain} | Mode: {'GOD-MODE' if settings.GOD_MODE_ENABLED else 'Standard'}")
    
    try:
        pipeline = ReconPipeline(domain=domain, wordlist=wordlist, concurrency=actual_concurrency)
        
        # Ensures a dedicated event loop for the async pipeline
        result = asyncio.run(pipeline.run())
        
        if result.get("status") == "SUCCESS":
            return {
                "domain": domain,
                "status": "COMPLETED",
                "critical_findings": result.get("critical_count", 0)
            }
        else:
            raise Exception(result.get("error", "Unknown Pipeline Error"))

    except Exception as exc:
        print(f"[NODE-ERROR] Failed {domain}: {exc}")
        raise self.retry(exc=exc, countdown=60)

def dispatch_mass_recon(domains: list, god_mode: bool = False):
    """
    Shards domains into the Redis queue.
    """
    print(f"[DISPATCHER] Sharding {len(domains)} domains (God-Mode: {god_mode})...")
    for domain in domains:
        run_distributed_recon.delay(domain)
    print("[DISPATCHER] All tasks successfully queued.")