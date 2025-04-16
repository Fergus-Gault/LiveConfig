import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[logging.StreamHandler()]
)

from .start_interface import start_interface
from .decorators import liveclass, liveinstance
from .liveconfig import LiveConfig