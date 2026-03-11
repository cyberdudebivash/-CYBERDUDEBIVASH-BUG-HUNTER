import asyncio
import redis
import json
from pipelines.recon_pipeline import ReconPipeline

r = redis.Redis(host="localhost", port=6379)


async def worker():
    while True:
        job = r.lpop("recon_jobs")

        if not job:
            await asyncio.sleep(1)
            continue

        data = json.loads(job)
        domain = data["domain"]

        pipeline = ReconPipeline(domain)
        await pipeline.run()


if __name__ == "__main__":
    asyncio.run(worker())