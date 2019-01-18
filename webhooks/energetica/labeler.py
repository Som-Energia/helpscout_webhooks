import aiohttp
import logging
import os
import psycopg2

from sanic import Blueprint
from sanic.response import json

import dbconfig as config

logger = logging.getLogger(__name__)

labeler = Blueprint("energetica_labeler", url_prefix="/energetica_labeler")


def relative(path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), path))


db = psycopg2.connect(**config.psycopg)
fd = open(relative('energetica_emails.sql'), 'r')
query = fd.read()


@labeler.route("/")
async def labelhook(request):

    with db.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    async with aiohttp.ClientSession() as session:
        async with session.get('https://aiohttp.readthedocs.io/en/stable/client_quickstart.html') as resp:
            print(resp.status)
            print(rows)
            helpscoutResponse = await resp.text()
    logger.debug(request.json)
    return json(helpscoutResponse, status=200)
