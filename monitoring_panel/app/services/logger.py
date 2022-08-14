import os
import logging

from ..settings import settings

LOGGING_FILE_PATH: str = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)
    ), '..', settings.LOGGING_FILENAME
)

if not os.path.exists(LOGGING_FILE_PATH):
    open(LOGGING_FILE_PATH, 'a').close()

if (
    os.path.getsize(LOGGING_FILE_PATH) // (1024 * 1024)
    >= settings.LOGGING_CLEAR_FILE_SIZE_LIMIT
):
    open(LOGGING_FILE_PATH, 'w').close()  # erase file content

logging.basicConfig(
    filename=os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
        ), '..', settings.LOGGING_FILENAME
    ),
    filemode='a+',
    format='%(asctime)s, %(msecs)d %(name)s %(levelname)s: %(message)s',
    datefmt='%H:%M:%S',
    level=settings.LOGGING_LEVEL
)
PANEL_LOGGER = logging.getLogger('PANEL')
