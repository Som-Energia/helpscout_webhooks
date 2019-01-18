import argparse
import asyncio
import logging
import sys


logger = logging.getLogger('hs_webhook')


def main(host, port):
    from webhooks.conf.startup_configuration import build_app

    loop = asyncio.get_event_loop()

    try:
        app, scheduler = loop.run_until_complete(build_app())

        logger.info("Running background tasks... ")
        scheduler.start()

        logger.info("Running helpscout webhooks... ")
        app.run(host, port)
    except (KeyboardInterrupt, SystemExit):
        logger.info("You kill me!!")
    except Exception as e:
        msg = "An uncontroled exception raised!!: %s"
        logger.exception(msg, str(e))
    finally:
        logger.info("Stopping helpscout webhooks :(")
        scheduler.shutdown()
        loop.close()
        sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Helpscout webhook service")

    parser.add_argument(
        "-H", "--host",
        help="host address to serve (default: %(default)r",
        type=str,
        default="localhost"
    )

    parser.add_argument(
        "-p", "--port",
        help="TCP/IP port to serve (default: %(default)r",
        type=str,
        default="8080"
    )

    args = parser.parse_args()

    main(args.host, args.port)
