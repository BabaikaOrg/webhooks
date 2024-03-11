import logging

from .common.util import config_logger

log = logging.getLogger(__name__)


async def init_app():
    """
    Initialize the app.
    """
    log.info("Initializing app...")
    config_logger()
    # TODO: DB bootstrap should be done by AWS ideally. This is a temporary solution.
    log.info("App initialized.")
