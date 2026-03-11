import asyncio
from automation.program_scope_manager import ProgramScopeManager
from automation.recon_worker import run_recon_worker


class TargetScheduler:

    def __init__(self, interval_hours=24):

        self.interval = interval_hours * 3600
        self.scope = ProgramScopeManager()

    async def run_cycle(self):

        targets = self.scope.get_all_targets()

        print(f"[Scheduler] Targets loaded: {len(targets)}")

        tasks = []

        for t in targets:

            domain = t["domain"]
            program = t["program"]

            print(f"[Scheduler] Queueing {domain}")

            task = asyncio.create_task(
                run_recon_worker(domain, program)
            )

            tasks.append(task)

        await asyncio.gather(*tasks)

    async def run(self):

        while True:

            print("[Scheduler] Starting recon cycle")

            await self.run_cycle()

            print("[Scheduler] Cycle completed")

            print(f"[Scheduler] Sleeping {self.interval}s")

            await asyncio.sleep(self.interval)


if __name__ == "__main__":

    scheduler = TargetScheduler(interval_hours=24)

    asyncio.run(scheduler.run())