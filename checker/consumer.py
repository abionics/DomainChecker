import asyncio
import json

from checker.db.database import Database
from checker.db.models import Domain
from checker.utils.punycode import Punycode
from config import CHECK_ABILITY_API_URL, NAME_API_USERNAME, NAME_API_PASSWORD
from mechanotopia.asynchronous.base.consumer import BaseConsumer
from mechanotopia.asynchronous.modules.fetcher import AsyncFetcher


class Consumer(BaseConsumer):
    def __init__(self, queue: asyncio.Queue):
        super().__init__(queue)
        self._fetcher = AsyncFetcher()
        self._db = Database()

    async def consume(self, task: dict):
        query = task['query']
        tlds = task['tlds']
        domains_names = list()
        for tld in tlds:
            domains_name = f'{query}.{tld}'
            domains_names.append(domains_name)
        data = json.dumps(domains_names)
        data = f'{{"domainNames": {data}}}'
        content = await self._fetcher.fetch('POST', CHECK_ABILITY_API_URL, data=data,
                                            auth=(NAME_API_USERNAME, NAME_API_PASSWORD))
        self.__save(content)

    def __save(self, content: str):
        results = json.loads(content)['results']
        for result in results:
            domains_name = Punycode.decode(result['domainName'])
            query = Punycode.decode(result['sld'])
            tld = Punycode.decode(result['tld'])
            purchasable = result.get('purchasable', False)
            premium = result.get('premium', False if purchasable else None)
            purchase_price = result.get('purchasePrice')
            purchase_type = result.get('purchaseType')
            renewal_price = result.get('renewalPrice')
            domain = Domain(
                domain_name=domains_name,
                query=query,
                tld=tld,
                purchasable=purchasable,
                premium=premium,
                purchase_price=purchase_price,
                purchase_type=purchase_type,
                renewal_price=renewal_price
            )
            self._db.save(domain)
        self._db.commit()
