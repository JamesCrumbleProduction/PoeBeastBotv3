from concurrent.futures import ThreadPoolExecutor

LINKING_SERVER_EXECUTOR = ThreadPoolExecutor(
    max_workers=1, thread_name_prefix='Server'
)
