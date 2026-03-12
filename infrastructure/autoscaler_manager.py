"""
CYBERDUDEBIVASH BUG HUNTER - Cloud Auto-Scaler
Path: infrastructure/autoscaler_manager.py
Purpose: Dynamically scales DigitalOcean worker nodes based on Redis queue length.
"""

import time
import requests
import aioredis
import asyncio
import logging
from typing import List

# Configuration - Move these to config.py or .env in production
DO_TOKEN = "YOUR_DIGITALOCEAN_API_TOKEN"
SSH_KEY_ID = "YOUR_SSH_KEY_ID"  # Get from 'doctl compute ssh-key list'
SNAPSHOT_ID = "YOUR_WORKER_SNAPSHOT_ID" # Snapshot of a ready-to-go worker node
REGION = "nyc3"
SIZE = "s-1vcpu-2gb" # Optimized for high-concurrency recon

# Scaling Thresholds
MIN_WORKERS = 1
MAX_WORKERS = 10
TASKS_PER_WORKER = 50 # Every 50 domains in queue triggers 1 new node

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [AUTOSCALER] - %(message)s')
logger = logging.getLogger(__name__)

class CloudAutoscaler:
    def __init__(self):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DO_TOKEN}"
        }
        self.redis_url = "redis://localhost:6379/0"

    def get_active_workers(self) -> List[str]:
        """Queries DigitalOcean API for active worker droplets."""
        url = "https://api.digitalocean.com/v2/droplets?tag_name=cdb-worker"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200:
            return [d["id"] for d in resp.json()["droplets"]]
        return []

    def create_worker(self):
        """Spins up a new Droplet from the pre-configured snapshot."""
        url = "https://api.digitalocean.com/v2/droplets"
        payload = {
            "name": f"cdb-worker-{int(time.time())}",
            "region": REGION,
            "size": SIZE,
            "image": SNAPSHOT_ID,
            "ssh_keys": [SSH_KEY_ID],
            "tags": ["cdb-worker"],
            "user_data": "#!/bin/bash\ncd /app && celery -A scheduler_engine worker -l info"
        }
        resp = requests.post(url, json=payload, headers=self.headers)
        if resp.status_code == 202:
            logger.info(f"Successfully triggered creation of worker node.")
        else:
            logger.error(f"Failed to create worker: {resp.text}")

    def destroy_worker(self, droplet_id: str):
        """Terminates an idle worker node."""
        url = f"https://api.digitalocean.com/v2/droplets/{droplet_id}"
        requests.delete(url, headers=self.headers)
        logger.info(f"Terminated idle worker node: {droplet_id}")

    async def get_queue_length(self) -> int:
        """Checks the current length of the 'celery' task queue in Redis."""
        redis = await aioredis.from_url(self.redis_url)
        # Assuming the default celery queue name
        length = await redis.llen("celery")
        await redis.close()
        return length

    async def run_scaling_loop(self):
        """Main loop: Poll queue and adjust capacity every 60 seconds."""
        logger.info("Auto-Scaler loop started. Monitoring Redis Swarm...")
        while True:
            try:
                queue_len = await self.get_queue_length()
                active_ids = self.get_active_workers()
                current_count = len(active_ids)
                
                # Logic: Calculate needed workers
                needed = max(MIN_WORKERS, min(MAX_WORKERS, (queue_len // TASKS_PER_WORKER) + 1))
                
                logger.info(f"Queue: {queue_len} | Active Nodes: {current_count} | Target Nodes: {needed}")

                if current_count < needed:
                    diff = needed - current_count
                    for _ in range(diff):
                        self.create_worker()
                elif current_count > needed and current_count > MIN_WORKERS:
                    # Destroy the oldest idle worker
                    self.destroy_worker(active_ids[0])

            except Exception as e:
                logger.error(f"Scaling Loop Error: {e}")
            
            await asyncio.sleep(60)

if __name__ == "__main__":
    scaler = CloudAutoscaler()
    asyncio.run(scaler.run_scaling_loop())