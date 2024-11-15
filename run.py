import argparse
import asyncio
import logging
import sys

from webhooks.lib.hs_api import HelpscoutSDK
from webhooks.lib.fs_api import FreescoutSDK
from webhooks.conf import settings

logger = logging.getLogger('scout_webhook')


def main(host, port):
    from webhooks.conf.startup_configuration import build_app

    loop = asyncio.get_event_loop()

    for scout in settings.SCOUTS:
        if scout == 'helpscout':
            sdk = HelpscoutSDK()
        if scout == 'freescout':
            sdk = FreescoutSDK()

        try:
            app = loop.run_until_complete(build_app(loop, sdk))

            logger.info("Running {} background tasks... ".format(scout))
            app.scheduler.start()

            logger.info("Running {} webhooks... ".format(scout))
            server = app.create_server(host, port)
            task = loop.create_task(server)
            loop.run_forever()
        except (KeyboardInterrupt, SystemExit):
            logger.info("You kill {}!!".format(scout))
        except Exception as e:
            msg = "An uncontroled exception raised in {}!!: %s".format(scout)
            logger.exception(msg, str(e))
        finally:
            logger.info("Stopping {} webhooks :(".format(scout))
            task.cancel()
            app.scheduler.shutdown()
            loop.close()
            sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scout webhook service")

    parser.add_argument(
        "-H", "--host",
        help="host address to serve (default: %(default)r",
        type=str,
        default="0.0.0.0"
    )

    parser.add_argument(
        "-p", "--port",
        help="TCP/IP port to serve (default: %(default)r",
        type=str,
        default="8080"
    )

    args = parser.parse_args()

    main(args.host, args.port)


