"""
CYBERDUDEBIVASH BUG HUNTER - Distributed Scheduler
Powered by Celery + Redis
Scale: 1,000+ Domains / 24-7 Continuous Monitoring
"""

from celery import Celery
from celery.schedules import crontab
from recon_pipeline import ReconPipeline
import asyncio

# Initialize Celery with Redis as the Broker and Backend
celery_app = Celery(
    "cyberdude_swarm",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1"
)

@celery_app.task(name="tasks.run_distributed_recon", bind=True, max_retries=3)
def run_distributed_recon(self, domain: str):
    """
    Worker Logic: Each worker picks one domain and runs 
    the full World-Class Recon Pipeline.
    """
    print(f"[Worker] Targeting: {domain}")
    try:
        # Run our production pipeline asynchronously
        pipeline = ReconPipeline(domain, "wordlists/subdomains_large.txt")
        asyncio.run(pipeline.run())
        return {"status": "SUCCESS", "domain": domain}
    except Exception as exc:
        # Auto-retry with exponential backoff if a network error occurs
        raise self.retry(exc=exc, countdown=60)

# --- 💰 High-Revenue Feature: Continuous Monitoring ---
celery_app.conf.beat_schedule = {
    'enterprise-hourly-monitor': {
        'task': 'tasks.run_distributed_recon',
        'schedule': crontab(minute=0, hour='*/1'), # Runs every hour
        'args': ("enterprise-client.com",)
    },
}