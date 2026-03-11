import asyncio
import os

from automation.recon_worker import run_recon_worker


class WorkerNode:

    def __init__(self):

        self.node_id = os.getenv("NODE_ID", "node-1")

    async def run(self, domain, program):

        print(f"[{self.node_id}] Processing {domain}")

        await run_recon_worker(domain, program)


async def start_worker():

    worker = WorkerNode()

    domain = os.getenv("TARGET_DOMAIN")
    program = os.getenv("TARGET_PROGRAM")

    await worker.run(domain, program)


if __name__ == "__main__":
    asyncio.run(start_worker())