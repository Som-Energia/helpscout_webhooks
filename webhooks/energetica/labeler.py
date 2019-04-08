import base64
import hmac
import logging

from sanic import Blueprint
from sanic import response

from webhooks.conf import settings


logger = logging.getLogger('energetica')

labeler = Blueprint("energetica_labeler", url_prefix="/energetica_labeler")


@labeler.middleware('request')
async def check_signature(request):

    request_signature = base64.encodebytes(hmac.new(
        settings.SECRET_KEY.encode(),
        request.body,
        'sha1'
    ).digest()).strip().decode()

    hs_signature = request.headers.get('x-helpscout-signature', '')

    if request_signature != hs_signature:
        return response.json({'error': 'Unauthorized'}, status=401)


@labeler.route("/", methods=['POST'])
async def labelhook(request):
    hsApi = request.app.hsApi

    body = request.json
    energetica_emails = request.app.dbUtils.get_energetica_emails()
    if body['customer']['email'] in energetica_emails:
        mailbox_id = await hsApi.get_mailbox('Energética Coop')
        await hsApi.change_mailbox(body['id'], mailbox_id['id'])

    return response.json({}, status=200)
