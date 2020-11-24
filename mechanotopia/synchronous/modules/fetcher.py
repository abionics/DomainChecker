import requests

from config import DEFAULT_ALLOW_CODES, DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT
from mechanotopia.abstract.modules.fetcher import AbstractFetcher


class SyncFetcher(AbstractFetcher):
    def fetch(self,
              method: str,
              url: str,
              allow_codes: tuple = DEFAULT_ALLOW_CODES,
              max_retries: int = DEFAULT_MAX_RETRIES,
              ignore_errors: bool = False,
              default_response: str = None,
              **kwargs) -> str:
        timeout = kwargs.pop('timeout', DEFAULT_TIMEOUT)
        for order in range(max_retries):
            try:
                response = requests.request(method, url, verify=False, timeout=timeout,  **kwargs)
                status_code = response.status_code
                if allow_codes and status_code in allow_codes:
                    return response.text
            except Exception:
                status_code = -1
        else:
            if ignore_errors is False:
                raise Exception(f'Too many retries for {url}, last status code is {status_code}')
        return default_response
