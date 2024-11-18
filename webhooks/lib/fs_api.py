import logging
import ujson
from urllib.request import urljoin
import aiohttp

from webhooks.conf import settings

logger = logging.getLogger('fs_api')


class FreescoutAPI(object):

    def __init__(self, host):
        self.host = host

    async def mailboxes(self):
        headers = {
            "X-FreeScout-API-Key": settings.FREESCOUT_API_KEY,
            "Accept": "application/json",
            "Content-Type": "application/json; charset=UTF-8",
        }

        url = urljoin(settings.FREESCOUT_HOST, '/api/mailboxes')
        try:
            async with aiohttp.ClientSession(raise_for_status=True) as session:
                async with session.get(url, headers=headers) as resp:
                    body = await resp.json()
                    return body.get('_embedded', {}).get('mailboxes', [])

        except aiohttp.ClientConnectionError as e:
            msg = 'Error making request %s. Reason: %s'
            logger.error(msg, url, str(e))



    async def change_mailbox(self, conversation_id, mailbox_id):
        headers = {
            "X-FreeScout-API-Key": settings.FREESCOUT_API_KEY,
            "Accept": "application/json",
            "Content-Type": "application/json; charset=UTF-8",
        }

        url = urljoin(settings.FREESCOUT_HOST, '/api/conversations/{}'.format(conversation_id))

        body = {
            "mailboxId": mailbox_id,
            "byUser": settings.FREESCOUT_ADMIN_USER_ID,
        }

        try:
            async with aiohttp.ClientSession(raise_for_status=True) as session:
                await session.put(
                    url, headers=headers, data=ujson.dumps(body)
                )
        except aiohttp.ClientConnectionError as e:
            msg = 'Error making request %s. Reason: %s'
            logger.error(msg, url, str(e))


class FreescoutSDK(object):

    _fs_api = FreescoutAPI(settings.FREESCOUT_HOST)
    
    # def __init__(self):
    #     self._fs_api = FreescoutAPI(settings.FREESCOUT_HOST)

    async def get_mailbox(self, name):
        found = False
        i = 0

        mailboxes = await self._fs_api.mailboxes()
        while not found and i < len(mailboxes):
            if name == mailboxes[i].get('name', ''):
                found = True
            else:
                i += 1

        return mailboxes[i] if found else {}

    async def change_mailbox(self, conversation_id, mailbox_id):
        await self._fs_api.change_mailbox(conversation_id, mailbox_id)
