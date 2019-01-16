import logging

from sanic import Blueprint
from sanic.response import json

logger = logging.getLogger(__name__)

labeler = Blueprint("energetica_labeler", url_prefix="/energetica_labeler")


@labeler.route("/")
async def labelhook(request):
    logger.debug(request.json)
    return json({}, status=200)
