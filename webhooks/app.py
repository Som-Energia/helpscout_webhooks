import asyncio
import logging

from webhooks.conf.startup_configuration import build_app

from .lib.hs_api import HelpscoutSDK
from .lib.fs_api import FreescoutSDK
from webhooks.conf import settings

logger = logging.getLogger('scout_webhook')


def start_app():

    for scout in settings.SCOUTS:
        if scout == 'helpscout':
            sdk = HelpscoutSDK()
        if scout == 'freescout':
            sdk = FreescoutSDK()

        loop = asyncio.get_event_loop()
        app = loop.run_until_complete(build_app(loop, sdk))

        logger.info("Running background tasks... ")
        app.ctx.scheduler.start()

        return app

app = start_app()
