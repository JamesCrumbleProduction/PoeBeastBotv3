# autopep8: off
import os 
import sys
updater_path: str = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 
    *['..','..', 'project_updater'] 
) 
sys.path.append(updater_path)
import updater 
sys.path.remove(updater_path)


from .server import app
from .settings import settings
from .services.logger import BOT_LOGGER
from .services.executor import SERVER_EXECUTOR
from .bot_components import BOT_INSTANCE

__all__ = (
    'app',
    'settings',
    'BOT_LOGGER',
    'BOT_INSTANCE',
    'SERVER_EXECUTOR',
)
