import asyncio
from vcr_unittest import VCRTestCase
from urllib.request import urljoin

from webhooks.conf import settings
from webhooks.lib.utils import TokenRenew


class TokenRenewTest(VCRTestCase):

    def test__renew_token(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        token = TokenRenew(
            urljoin(settings.HELPSCOUT_HOST, '/v2/oauth2/token')
        )

        loop.run_until_complete(
            token.renew_token(token)
        )

        self.assertEqual(len(self.cassette), 1)
        self.assertEqual(self.cassette.responses[0]['status']['code'], 200)
        self.assertEqual(self.cassette.requests[0].uri, 'https://api.helpscout.net/v2/oauth2/token')
