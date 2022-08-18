import logging

logging.basicConfig(
    format='%(asctime)s, %(msecs)d %(name)s %(levelname)s: %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO
)

UPDATER_LOGGER = logging.getLogger('UPDATER')
