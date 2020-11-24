import asyncio
from abc import abstractmethod


class BaseProducer:
    def __init__(self, queue: asyncio.Queue):
        self._queue = queue

    @abstractmethod
    async def produce(self, **kwargs):
        pass
