from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from sanic import Sanic

from webhooks.energetica.labeler import labeler
from webhooks.lib.utils import dbUtils

from ..lib.hs_api import HelpscoutSDK


async def build_app(loop):
    import webhooks.conf.settings as settings

    app = Sanic(log_config=settings.LOGGING)
    app.hsApi = HelpscoutSDK()
    app.dbUtils = dbUtils()
    app.blueprint(labeler)
    app.scheduler = AsyncIOScheduler(event_loop=loop)

    app.scheduler.add_job(
        app.hsApi._hs_api.token_renew.renew_token,
        'interval',
        minutes=settings.TOKEN_TIME_REFRESH,
        max_instances=1,
        next_run_time=datetime.now(),
        args=[app.hsApi._hs_api.token_renew]
    )
    app.scheduler.add_job(
        app.dbUtils.refresh_local_email_list,
        'interval',
        minutes=settings.TOKEN_TIME_REFRESH,
        max_instances=1,
        next_run_time=datetime.now(),
        args=[app.dbUtils]
    )

    return app
