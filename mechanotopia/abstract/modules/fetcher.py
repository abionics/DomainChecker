from abc import abstractmethod

from config import DEFAULT_ALLOW_CODES, DEFAULT_MAX_RETRIES


class AbstractFetcher:
    @abstractmethod
    def fetch(self,
              method: str,
              url: str,
              allow_codes: tuple = DEFAULT_ALLOW_CODES,
              max_retries: int = DEFAULT_MAX_RETRIES,
              ignore_errors: bool = False,
              default_response: str = None,
              **kwargs) -> str:
        pass
