import argparse
import asyncio
import logging
import sys


logger = logging.getLogger('hs_webhook')


def main(host, port):
    from webhooks.conf.startup_configuration import build_app

    loop = asyncio.get_event_loop()

    try:
        app = loop.run_until_complete(build_app(loop))

        logger.info("Running background tasks... ")
        app.scheduler.start()

        logger.info("Running helpscout webhooks... ")
        server = app.create_server(host, port)
        task = loop.create_task(server)
        loop.run_forever()
    except (KeyboardInterrupt, SystemExit):
        logger.info("You kill me!!")
    except Exception as e:
        msg = "An uncontroled exception raised!!: %s"
        logger.exception(msg, str(e))
    finally:
        logger.info("Stopping helpscout webhooks :(")
        task.cancel()
        app.scheduler.shutdown()
        loop.close()
        sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Helpscout webhook service")

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
