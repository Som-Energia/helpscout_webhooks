import logging
import ujson
from urllib.request import urljoin

import aiohttp

from webhooks.conf import settings
from .utils import TokenRenew


logger = logging.getLogger('hs_api')


class HelpscoutAPI(object):

    endpoints = {
        'token': '/v2/oauth2/token',
        'mailboxes': '/v2/mailboxes',
        'change_mailbox': '/v2/conversations'
    }

    def __init__(self, host):
        self.host = host
        self.token_renew = TokenRenew(urljoin(self.host, self.endpoints['token']))

    async def mailboxes(self):
        headers = {
            'Authorization': 'bearer {}'.format(self.token_renew.token)
        }
        url = urljoin(self.host, self.endpoints['mailboxes'])

        try:
            async with aiohttp.ClientSession(raise_for_status=True) as session:
                async with session.get(url, headers=headers) as resp:
                    return await resp.json().get('_embedded', [])
        except aiohttp.ClientConnectionError as e:
            msg = 'Error making request %s. Reason: %s'
            logger.error(msg, url, str(e))

    async def change_mailbox(self, conversation_id, mailbox_id):
        headers = {
            'Authorization': 'bearer {}'.format(self.token_renew.token),
            'Content-type': 'application/json'
        }

        url = ''.join([
                        self.host,
                        self.endpoints['change_mailbox'],
                        '/',
                        str(conversation_id)
                ])

        body = {'op': 'move', 'path': '/mailboxId', 'value': mailbox_id}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.patch(url, headers=headers, data=ujson.dumps(body)) as resp:
                    pass
        except aiohttp.ClientConnectionError as e:
            msg = 'Error making request %s. Reason: %s'
            logger.error(msg, url, str(e))



class HelpscoutSDK(object):

    def __init__(self):
        self._hs_api = HelpscoutAPI(settings.HELPSCOUT_HOST)

    async def get_mailbox(self, name):
        found = False
        i = 0

        mailboxes = await self._hs_api.mailboxes()
        while not found and i < len(mailboxes):
            found = name == mailboxes[i].get('name', '')
            i += 1

        return mailboxes[i] if found else {}

    async def change_mailbox(self, conversation_id, mailbox_id):

            await self._hs_api.change_mailbox(conversation_id, mailbox_id)
