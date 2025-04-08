from liveconfig.manager import LiveManager
import logging

manager = LiveManager()

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
