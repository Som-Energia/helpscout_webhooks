import logging
import ujson
import os

import aiohttp
import psycopg2

from webhooks.conf import settings

logger = logging.getLogger('hs_webhook')


def relative(path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), path))


class TokenRenew(object):

    def __init__(self, url):
        self.url = url
        self.body = {
            'grant_type': 'client_credentials',
            'client_id': settings.CLIENT_ID,
            'client_secret': settings.CLIENT_SECRET
        }
        self.headers = {
            'content-type': 'application/json'
        }
        self.token = ''

    @staticmethod
    async def renew_token(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.url, headers=self.headers, data=ujson.dumps(self.body)) as resp:
                    body = await resp.json()
                    self.token = body['access_token']
        except aiohttp.ClientConnectionError as e:
            msg = 'Error making request %s. Reason: %s'
            logger.error(msg, url, str(e))


class dbUtils(object):

    def __init__(self):
        self.energetica_emails = []
        self.sql_attributes = settings.SQL

    def get_energetica_emails(self):
        return self.energetica_emails

    @staticmethod
    def refresh_local_email_list(self):
        self.db = psycopg2.connect(**settings.DATABASE)
        fd = open(relative('sql/energetica_emails.sql'), 'r')
        query = fd.read()
        query = query.format(self.sql_attributes['energetica_emails'])
        with self.db.cursor() as cursor:
            cursor.execute(query)
            emails = cursor.fetchone()
        self.energetica_emails = emails
