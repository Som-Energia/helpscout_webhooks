import asyncio

from vcr_unittest import VCRTestCase

from webhooks.conf import settings
from webhooks.lib.hs_api import HelpscoutSDK, HelpscoutAPI


class HelpscoutSDKTest(VCRTestCase):

    def test__change_mailbox(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        hs_sdk = HelpscoutSDK()

        loop.run_until_complete(
            hs_sdk._hs_api.token_renew.renew_token(hs_sdk._hs_api.token_renew)
        )
        loop.run_until_complete(
            hs_sdk.change_mailbox(762899217, 93840)
        )

        self.assertEqual(len(self.cassette), 2)
        self.assertEqual(self.cassette.responses[0]['status']['code'], 200)
        self.assertEqual(self.cassette.responses[1]['status']['code'], 204)

    def test__get_mailbox(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        hs_sdk = HelpscoutSDK()

        loop.run_until_complete(
            hs_sdk._hs_api.token_renew.renew_token(hs_sdk._hs_api.token_renew)
        )
        loop.run_until_complete(
            hs_sdk.get_mailbox(5678)
        )

        self.assertEqual(len(self.cassette), 2)
        self.assertEqual(self.cassette.responses[0]['status']['code'], 200)
        self.assertEqual(self.cassette.responses[1]['status']['code'], 200)


class HelpscoutAPITest(VCRTestCase):

    def test__change_mailbox(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        hs_api = HelpscoutAPI(settings.HELPSCOUT_HOST)

        loop.run_until_complete(
            hs_api.token_renew.renew_token(hs_api.token_renew)
        )
        loop.run_until_complete(
            hs_api.change_mailbox(762899217, 93840)
        )

        self.assertEqual(len(self.cassette), 2)
        self.assertEqual(self.cassette.responses[0]['status']['code'], 200)
        self.assertEqual(self.cassette.responses[1]['status']['code'], 204)

    def test__mailboxes(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        hs_api = HelpscoutAPI(settings.HELPSCOUT_HOST)

        loop.run_until_complete(
            hs_api.token_renew.renew_token(hs_api.token_renew)
        )
        loop.run_until_complete(
            hs_api.mailboxes()
        )

        self.assertEqual(len(self.cassette), 2)
        self.assertEqual(self.cassette.responses[0]['status']['code'], 200)
        self.assertEqual(self.cassette.responses[1]['status']['code'], 200)
