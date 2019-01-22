import logging
from urllib.request import urljoin

import aiohttp

from webhooks.conf import settings
from .utils import TokenRenew


logger = logging.getLogger('hs_api')


class HelpscoutAPI(object):

    endpoints = {
        'mailboxes': '/v2/mailboxes'
    }

    def __init__(self, host):
        self.host = host
        self.token_renew = TokenRenew()

    def change_mailbox(self, conversationId, mailboxId):
        # Patch request
        pass

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
