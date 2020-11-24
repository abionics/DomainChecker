import asyncio
import logging
from typing import Type

from mechanotopia.asynchronous.base.consumer import BaseConsumer
from mechanotopia.asynchronous.base.producer import BaseProducer


class AsyncScraper:
    def __init__(self,
                 producer_class: Type[BaseProducer],
                 consumer_class: Type[BaseConsumer],
                 producers_count: int,
                 consumers_count: int,
                 **producer_kwargs):
        self._producer_class = producer_class
        self._consumer_class = consumer_class
        self._producers_count = producers_count
        self._consumers_count = consumers_count
        self._producer_kwargs = producer_kwargs
        self._queue = asyncio.Queue()
        self._logger = logging.getLogger('[asynchronous][scraper]')

    def run_sync(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run())

    async def run(self):
        producers = self.__create_coroutines(self.__create_producer, self._producers_count, **self._producer_kwargs)
        consumers = self.__create_coroutines(self.__create_consumer, self._consumers_count)

        await asyncio.gather(*producers)
        await self._queue.join()

        for consumer in consumers:
            consumer.cancel()

    @staticmethod
    def __create_coroutines(function, count: int, **kwargs) -> list:
        return [asyncio.create_task(function(**kwargs))
                for _ in range(count)]

    async def __create_producer(self, **kwargs):
        producer = self._producer_class(self._queue)
        await producer.produce(**kwargs)

    async def __create_consumer(self):
        consumer = self._consumer_class(self._queue)
        while True:
            task = await self._queue.get()
            await self.process_task(consumer, task)
            self._queue.task_done()

    async def process_task(self, consumer: BaseConsumer, task: dict):
        try:
            await consumer.consume(task)
        except Exception as e:
            self._logger.exception(e)
