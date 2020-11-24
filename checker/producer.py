from config import TLDS_COUNT_PER_REQUEST
from mechanotopia.asynchronous.base.producer import BaseProducer


class Producer(BaseProducer):
    async def produce(self, query: str, tlds: list):
        groups = self.__group(tlds, TLDS_COUNT_PER_REQUEST)
        for group in groups:
            task = {
                'query': query,
                'tlds': group,
            }
            await self._queue.put(task)

    @staticmethod
    def __group(lst: list, size: int) -> list:
        return [
            lst[i:i + size]
            for i in range(0, len(lst), size)
        ]
