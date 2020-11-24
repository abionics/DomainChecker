import httpx

from config import DEFAULT_ALLOW_CODES, DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT
from mechanotopia.abstract.modules.fetcher import AbstractFetcher


class AsyncFetcher(AbstractFetcher):
    async def fetch(self,
                    method: str,
                    url: str,
                    allow_codes: tuple = DEFAULT_ALLOW_CODES,
                    max_retries: int = DEFAULT_MAX_RETRIES,
                    ignore_errors: bool = False,
                    default_response: str = None,
                    **kwargs) -> str:
        proxies = kwargs.pop('proxies', None)
        timeout = kwargs.pop('timeout', DEFAULT_TIMEOUT)
        for order in range(max_retries):
            try:
                async with httpx.AsyncClient(proxies=proxies, verify=False, timeout=timeout) as client:
                    response = await client.request(method, url, **kwargs)
                    status_code = response.status_code
                    if allow_codes and status_code in allow_codes:
                        return response.text
            except Exception:
                status_code = -1
        else:
            if ignore_errors is False:
                raise Exception(f'Too many retries for {url}, last status code is {status_code}')
        return default_response
