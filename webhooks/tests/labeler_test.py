from webhooks.app import app

import json
import unittest
from asyncio import coroutine
from unittest import mock
from unittest.mock import MagicMock
from vcr_unittest import VCRTestCase


def AsyncMock(*args, **kwargs):
    import unittest

    m = mock.MagicMock(*args, **kwargs)

    async def mock_coro(*args, **kwargs):
        return m(*args, **kwargs)

    mock_coro.mock = m
    return mock_coro

class LabelerTest(unittest.TestCase):

    def test__you_can_not_pass(self):
        body = {
            'customer': {'email': 'example@example.com'},
            'id': 1234
        }

        app.test_client.post('/energetica_labeler',
                             data=json.dumps(body),
                             headers={'x-helpscout-signature': 'OVdmCjJeaW/zzSP/A5T/Y9XXxWY='})


    @mock.patch('webhooks.lib.hs_api.HelpscoutSDK.get_mailbox', new=AsyncMock(return_value={'id': 5001}))
    def test__energetica_mail(self):
        body = {
            'customer': {'email': 'example@example.com'},
            'id': 1234
        }
        app.dbUtils.get_energetica_emails = MagicMock(
            return_value=['example@example.com']
        )
        app.hsApi.change_mailbox = MagicMock()

        app.test_client.post(
            '/energetica_labeler',
            data=json.dumps(body),
            headers={'x-helpscout-signature': 'OVdmCjJeaW/zzSP/A5T/Y9XXxWY='}
        )
        app.hsApi.change_mailbox.assert_called_once_with(1234, 5001)


    def test__no_energetica_mail(self):
        body = {
            'customer': {'email': 'example@example.com'},
            'id': 1234
        }
        app.dbUtils.get_energetica_emails = MagicMock(return_value=['diferent@example.com'])

        app.hsApi.get_mailbox = MagicMock()

        request, response = app.test_client.post('/energetica_labeler',
                                    data=json.dumps(body),
                                    headers={'x-helpscout-signature': 'OVdmCjJeaW/zzSP/A5T/Y9XXxWY='})

        self.assertEquals(200, response.status)
        app.hsApi.get_mailbox.assert_not_called()
