import logging
import os

# Fetcher
DEFAULT_ALLOW_CODES = (200, 201, 202, 203, 204)
DEFAULT_MAX_RETRIES = 5
DEFAULT_TIMEOUT = 30

# Async params
PRODUCERS_COUNT = 1
CONSUMERS_COUNT = 10

# Credentials for https://www.name.com
NAME_API_USERNAME = os.getenv('NAME_API_USERNAME')
NAME_API_PASSWORD = os.getenv('NAME_API_PASSWORD')

# Custom
LOGGING_LEVEL = logging.INFO
DATABASE_CONNECTION_URL = 'sqlite:///db.sqlite'
REPORTS_DIRECTORY = 'reports'

TLDS_LIST_URL = 'https://www.name.com/domains'
TLDS_COUNT_PER_REQUEST = 50
CHECK_ABILITY_API_URL = 'https://api.name.com/v4/domains:checkAvailability'
