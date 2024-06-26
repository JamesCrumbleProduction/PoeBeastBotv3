# autopep8: off
import os
import sys

from .settings import settings

if settings.AUTO_UPDATE is True:
    updater_path: str = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        *['..','..', 'project_updater'] 
    ) 
    sys.path.append(updater_path)
    import updater 
    sys.path.remove(updater_path)

from .panels import GuiSelector
from .linking_server import LinkingServer

__all__ = (
    'settings',
    'GuiSelector',
    'LinkingServer',
)
