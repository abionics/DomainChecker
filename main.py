import json
import logging
import re

from checker.consumer import Consumer
from checker.producer import Producer
from checker.report import create_report
from checker.utils.punycode import Punycode
from config import PRODUCERS_COUNT, CONSUMERS_COUNT, LOGGING_LEVEL, TLDS_LIST_URL
from mechanotopia.asynchronous.scraper import AsyncScraper
from mechanotopia.synchronous.modules.fetcher import SyncFetcher

# QUERIES = ['data', 'abionics']
# QUERIES = ['abi', 'dev', 'test', 'shop', 'casino']
QUERIES = ['money', 'vip', 'store', 'bank', 'sell', 'buy', 'me']
# QUERIES = ['kizuto']

logging.basicConfig(level=LOGGING_LEVEL, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('[main]')


def scrape(queries: list):
    tlds = _extract_tlds(TLDS_LIST_URL)
    logger.info(f'Total tlds count is {len(tlds)}')
    for query in queries:
        logger.info(f'Start scraping query "{query}"')
        scraper = AsyncScraper(Producer, Consumer, PRODUCERS_COUNT, CONSUMERS_COUNT, query=query, tlds=tlds)
        scraper.run_sync()
        logger.info(f'Successful scraped query "{query}"')


def report(queries: list):
    for query in queries:
        create_report(query)
        logger.info(f'Successful created report for query "{query}"')


def _extract_tlds(url: str) -> list:
    fetcher = SyncFetcher()
    content = fetcher.fetch('GET', url)
    content = content.replace('\n', ' ')
    data = re.findall(r'this\.tlds = new Tlds\((.*?)\);', content)[0]
    data = json.loads(data)
    tlds = list()
    for d in data:
        tld = d['tld']
        is_supported = d['is_supported']
        if is_supported:
            tld = Punycode.decode(tld)
            tlds.append(tld)
    return tlds


if __name__ == '__main__':
    scrape(QUERIES)
    report(QUERIES)
