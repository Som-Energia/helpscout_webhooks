import asyncio
import logging

from webhooks.conf.startup_configuration import build_app


logger = logging.getLogger('hs_webhook')


def start_app():
    loop = asyncio.get_event_loop()
    app, scheduler = loop.run_until_complete(build_app())

    logger.info("Running background tasks... ")
    scheduler.start()

    return app

app = start_app()
