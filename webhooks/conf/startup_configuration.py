from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from datetime import datetime
from sanic import Sanic

from webhooks.energetica.labeler import labeler_hs, labeler_fs
from webhooks.lib.utils import dbUtils
from webhooks.lib.hs_api import HelpscoutSDK
from webhooks.lib.fs_api import FreescoutSDK

async def build_app(loop, scout):
    import webhooks.conf.settings as settings

    app = Sanic('ScoutWebhooks',log_config=settings.LOGGING)

    app.scoutApi = scout
    app.dbUtils = dbUtils()

    if type(app.scoutApi) == HelpscoutSDK:
        app.blueprint(labeler_hs)
        app.scheduler = AsyncIOScheduler(event_loop=loop)

        app.scheduler.add_job(
            app.scoutApi._hs_api.token_renew.renew_token,
            'interval',
            minutes=settings.TOKEN_TIME_REFRESH,
            max_instances=1,
            next_run_time=datetime.now(),
            args=[app.hsApi._hs_api.token_renew]
        )

    if type(app.scoutApi) == FreescoutSDK:
        app.blueprint(labeler_fs)
        app.scheduler = AsyncIOScheduler(event_loop=loop)

    app.scheduler.add_job(
        app.dbUtils.refresh_local_email_list,
        CronTrigger(hour=0),
        max_instances=1,
        next_run_time=datetime.now(),
        args=[app.dbUtils]
    )

    return app
