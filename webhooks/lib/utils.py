import logging
import ujson
import os

import aiohttp
import psycopg2

from webhooks.conf import settings

logger = logging.getLogger('scout_webhook')


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
        logger.info('Renewing helpscout access token')
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.url, headers=self.headers, data=ujson.dumps(self.body)
                ) as resp:
                    body = await resp.json()
                    self.token = body['access_token']
        except aiohttp.ClientConnectionError as e:
            msg = 'Error making request %s. Reason: %s'
            logger.error(msg, self.url, str(e))
        else:
            logger.info('Renewing helpscout access token finish')


class dbUtils(object):

    def __init__(self):
        self.energetica_emails = []
        self.sql_attributes = settings.SQL
        self.domain_exception = settings.DOMAIN_EXCEPTION

    def get_energetica_emails(self):
        return self.energetica_emails

    @staticmethod
    def refresh_local_email_list(self):
        logger.info('Refreshing energetica emails list')

        before_refresh_emails_length = len(self.energetica_emails)
        with open(relative('sql/energetica_emails.sql'), 'r') as f:
            query_str = f.read()

        with psycopg2.connect(**settings.DATABASE) as db_conn:
            with db_conn.cursor() as cursor:
                cursor.execute(query_str, (self.sql_attributes['energetica_emails'],))
                emails = cursor.fetchall()

        self.energetica_emails = set([
            elem[0] for elem in emails
            if self.domain_exception not in elem[0]
        ])
        after_refresh_emails_length = len(self.energetica_emails)

        logger.debug(
            'There was %d emails, now there are %d',
            before_refresh_emails_length,
            after_refresh_emails_length
        )
