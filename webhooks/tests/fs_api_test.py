import asyncio

from vcr_unittest import VCRTestCase

from webhooks.conf import settings
from webhooks.lib.fs_api import FreescoutAPI, FreescoutSDK

class FreescoutSDKTest(VCRTestCase):

    def test__mailboxes(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        fs_sdk = FreescoutSDK()
        target_mailbox = "Demo Mailbox"
        mailbox = loop.run_until_complete(
            fs_sdk.get_mailbox(target_mailbox)    
        )

        self.assertEqual(mailbox['name'], target_mailbox)
        self.assertEqual(self.cassette.responses[0]['status']['code'], 200)


class FreescoutAPITest(VCRTestCase):

    def test__mailboxes(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        fs_api = FreescoutAPI(settings.FREESCOUT_HOST)
        loop.run_until_complete(
            fs_api.mailboxes()    
        )

        self.assertGreaterEqual(len(self.cassette.responses), 1)
        self.assertEqual(self.cassette.responses[0]['status']['code'], 200)

    def test__change_mailbox(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        hs_api = FreescoutAPI(settings.FREESCOUT_HOST)

        loop.run_until_complete(
            hs_api.change_mailbox(11, 3)
        )
        
        self.assertEqual(self.cassette.responses[0]['status']['code'], 204)