from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sanic import Sanic

from webhooks.energetica.labeler import labeler
from webhooks.lib.utils import TokenRenew


async def build_app():
    import webhooks.conf.settings as settings

    app = Sanic(log_config=settings.LOGGING)
    app.blueprint(labeler)

    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        TokenRenew().renew_token,
        'interval',
        minutes=settings.TOKEN_TIME_REFRESH,
        max_instances=1
    )

    return app, scheduler
