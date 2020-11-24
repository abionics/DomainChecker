import asyncio
from abc import abstractmethod


class BaseConsumer:
    def __init__(self, queue: asyncio.Queue):
        self._queue = queue

    @abstractmethod
    async def consume(self, task: dict):
        pass
