from concurrent.futures import ThreadPoolExecutor

from ..settings import settings

REQUESTS_EXECUTOR = ThreadPoolExecutor(
    max_workers=settings.WORKERS, thread_name_prefix='REQUESTS_EXECUTOR'
)

SERVER_EXECUTOR = ThreadPoolExecutor(
    max_workers=1, thread_name_prefix='SERVER_EXECUTOR'
)
