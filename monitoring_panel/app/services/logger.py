import os
import logging

from ..settings import settings

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
