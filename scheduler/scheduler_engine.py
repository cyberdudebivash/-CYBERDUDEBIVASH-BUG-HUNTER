"""
CYBERDUDEBIVASH BUG HUNTER - Distributed Scheduler Engine
Path: scheduler/scheduler_engine.py
Architecture: Celery + Redis + Asyncio
Purpose: High-Concurrency Multi-Domain Orchestration for 1,000+ Targets
"""

import asyncio
from celery import Celery
from celery.signals import worker_process_init
from pipelines.recon_pipeline import ReconPipeline

# 1. Initialize Celery with Redis as the Broker and Backend
# High-Profit Logic: Redis handles the 'Queue', Celery handles the 'Work'
celery_app = Celery(
    "cyberdude_swarm",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1"
)

# 2. Advanced Enterprise Configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    worker_prefetch_multiplier=1,      # Prevents one worker from hoarding all tasks
    task_acks_late=True,                # Ensures tasks are re-queued if a worker crashes
    task_time_limit=3600,               # 1-hour hard limit per domain scan
    worker_max_tasks_per_child=10       # Recycles workers to prevent memory leaks
)

@celery_app.task(name="tasks.run_distributed_recon", bind=True, max_retries=3)
def run_distributed_recon(self, domain: str, wordlist: str = "wordlists/subdomains_top1000.txt"):
    """
    The Swarm Task: Executes the full world-class pipeline for a single target.
    Bridges the Synchronous Celery environment with the Asynchronous Recon Pipeline.
    """
    print(f"[SWARM-NODE] Received Target: {domain}")
    
    try:
        # Initializing the Enterprise Pipeline
        pipeline = ReconPipeline(domain=domain, wordlist=wordlist)
        
        # Bridge Sync to Async
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(pipeline.run())
        
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
        run_distributed_recon.delay(domain)
    print("[DISPATCHER] All tasks successfully queued in Redis.")