import asyncio
import logging

from webhooks.conf.startup_configuration import build_app

from .lib.hs_api import HelpscoutSDK
from .lib.fs_api import FreescoutSDK
from webhooks.conf import settings

logger = logging.getLogger('scout_webhook')


def start_app():
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(build_app(loop, FreescoutSDK()))

    logger.info("Running background tasks... ")
    app.scheduler.start()

    return app

app = start_app()
