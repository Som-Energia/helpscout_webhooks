import logging
import os

import psycopg2

from webhooks.conf import settings

logger = logging.getLogger('hs_webhook')


def relative(path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), path))


class TokenRenew(object):

    def __init__(self):
        pass
        self.token = ''

    @staticmethod
    def renew_token():
        pass


class dbUtils(object):

    def __init__(self):
        self.db = psycopg2.connect(**settings.DATABASE)

    def energeticaMails(self):
        fd = open(relative('sql/energetica_emails.sql'), 'r')
        query = fd.read()
        with self.db.cursor() as cursor:
            cursor.execute(query)
            emails = cursor.fetchone()
        return emails
