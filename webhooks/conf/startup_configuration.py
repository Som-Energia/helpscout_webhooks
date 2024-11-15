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

    app.ctx.scoutApi = scout
    app.ctx.dbUtils = dbUtils()

    if type(app.ctx.scoutApi) == HelpscoutSDK:
        app.blueprint(labeler_hs)
        app.ctx.scheduler = AsyncIOScheduler(event_loop=loop)

        app.ctx.scheduler.add_job(
            app.ctx.scoutApi._hs_api.token_renew.renew_token,
            'interval',
            minutes=settings.TOKEN_TIME_REFRESH,
            max_instances=1,
            next_run_time=datetime.now(),
            args=[app.ctx.hsApi._hs_api.token_renew]
        )

    if type(app.ctx.scoutApi) == FreescoutSDK:
        app.blueprint(labeler_fs)
        app.ctx.scheduler = AsyncIOScheduler(event_loop=loop)

    app.ctx.scheduler.add_job(
        app.ctx.dbUtils.refresh_local_email_list,
        CronTrigger(hour=0),
        max_instances=1,
        next_run_time=datetime.now(),
        args=[app.ctx.dbUtils]
    )

    return app
