import asyncio
from functools import wraps

from pymongo.errors import ConnectionFailure, NetworkTimeout, PyMongoError

from api.core import constants as cons


def retry(times: int, backoff: float = cons.BACKOFF_FACTOR):
    """
    Decorator to retry async MongoDB operations on connection errors.

    :param times: number of times to retry operation on.
    :type times: int
    :param backoff: backoff factor to wait for next request.
    :type backoff: float
    """

    def func_wrapper(fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return await fn(*args, **kwargs)
                except (ConnectionFailure, NetworkTimeout):
                    if attempt < times:
                        delay = backoff * 2 ** (attempt - 1)
                        await asyncio.sleep(delay)
            raise PyMongoError(f"Operation failed after {attempt} retries")

        return wrapper

    return func_wrapper
