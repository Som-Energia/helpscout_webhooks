from webhooks.app import app

import json
import unittest
from unittest import mock
from unittest.mock import MagicMock
from webhooks.conf import settings


def AsyncMock(*args, **kwargs):

    m = mock.MagicMock(*args, **kwargs)

    async def mock_coro(*args, **kwargs):
        return m(*args, **kwargs)

    mock_coro.mock = m
    return mock_coro


class FreescoutLabelerTest(unittest.TestCase):

    def test__you_can_not_pass(self):
        body = {
            'primaryCustomer': {'email': 'example@example.com'},
            'id': 1234
        }

        request, response = app.test_client.post(
            '/energetica_labeler',
            data=json.dumps(body),
            headers={'x-freescout-signature': 'wrongsignature'}
        )

    @mock.patch('webhooks.lib.fs_api.FreescoutSDK.get_mailbox', new=AsyncMock(return_value={'id': 5001}))
    def test__energetica_mail(self):
        body = {
            'primaryCustomer': {'email': 'example@example.com'},
            'id': 1234
        }
        app.ctx.dbUtils.get_energetica_emails = MagicMock(
            return_value=['example@example.com']
        )

        app.ctx.scoutApi.change_mailbox = AsyncMock()

        request, response = app.test_client.post(
            '/energetica_labeler',
            data=json.dumps(body),
            headers={'x-freescout-signature': settings.FREESCOUT_WEBHOOK_SIGNATURE}
        )
        app.ctx.scoutApi.change_mailbox.mock.assert_called_once_with(1234, 5001)

    def test__no_energetica_mail(self):
        body = {
            'primaryCustomer': {'email': 'example@example.com'},
            'id': 1234
        }
        app.ctx.dbUtils.get_energetica_emails = MagicMock(
            return_value=['diferent@example.com']
        )

        app.ctx.scoutApi.get_mailbox = MagicMock()

        request, response = app.test_client.post(
            '/energetica_labeler',
            data=json.dumps(body),
            headers={'x-freescout-signature': settings.FREESCOUT_WEBHOOK_SIGNATURE}
        )

        app.ctx.scoutApi.get_mailbox.assert_not_called()
        self.assertEqual(200, response.status)
