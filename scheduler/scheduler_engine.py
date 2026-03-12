"""
CYBERDUDEBIVASH BUG HUNTER - Distributed Scheduler Engine
Path: scheduler/scheduler_engine.py
Architecture: Celery + Redis + Asyncio
Purpose: High-Concurrency Multi-Domain Orchestration for 1,000+ Targets
"""

import asyncio
import logging
from celery import Celery
from pipelines.recon_pipeline import ReconPipeline
from config import settings

# --- 1. Initialize Celery Swarm Core ---
# High-Profit Logic: Redis handles the 'Queue', Celery handles the 'Work'
celery_app = Celery(
    "cyberdude_swarm",
    broker=settings.REDIS_URL,
    backend="redis://localhost:6379/1"
)

# --- 2. Advanced Enterprise Configuration ---
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    worker_prefetch_multiplier=1,      # Prevents one worker from hoarding all tasks
    task_acks_late=True,               # Ensures tasks are re-queued if a worker crashes
    task_time_limit=3600,              # 1-hour hard limit per domain scan
    worker_max_tasks_per_child=10,     # Recycles workers to prevent memory leaks
    broker_connection_retry_on_startup=True
)

@celery_app.task(name="tasks.run_distributed_recon", bind=True, max_retries=3)
def run_distributed_recon(self, domain: str, wordlist: str = None):
    """
    The Swarm Task: Robustly bridges Sync Celery with Async ReconPipeline.
    Uses asyncio.run() to ensure a fresh, dedicated event loop for every target.
    """
    if wordlist is None:
        wordlist = settings.DEFAULT_WORDLIST

    print(f"[SWARM-NODE] Received Target: {domain}")
    
    try:
        # Initializing the Enterprise Pipeline
        pipeline = ReconPipeline(domain=domain, wordlist=wordlist)
        
        # PRODUCTION FIX: Explicitly create a new event loop for this thread.
        # This resolves the 'There is no current event loop' error in Celery workers.
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
        # Exponential backoff retry logic (1m, 2m, 4m...)
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))

def dispatch_mass_recon(domains: list):
    """
    Highest Max Profit Logic:
    Takes a list of 1,000+ domains and shards them into the Redis queue.
    """
    print(f"[DISPATCHER] Sharding {len(domains)} domains into the global swarm...")
    for domain in domains:
        # .delay() pushes the task to Redis immediately
        run_distributed_recon.delay(domain)
    print("[DISPATCHER] All tasks successfully queued in Redis.")