import asyncio


class ReconOrchestrator:

    def __init__(self):
        self.tasks = []

    def add_task(self, coro):
        self.tasks.append(coro)

    async def run(self):

        if not self.tasks:
            print("No tasks registered")
            return

        print(f"[CORE] Running {len(self.tasks)} pipeline stages")

        for task in self.tasks:

            try:
                await task

            except Exception as e:
                print(f"[CORE] Stage failed: {e}")