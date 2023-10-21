import asyncio

from leon import Leon


class Forks:
    def __init__(self):
        self.fonbet = None
        self.leon = Leon()

    async def run(self):
        tasks = []
        tasks.append(asyncio.create_task(self.leon.get_line()))
        await asyncio.gather(*tasks)
