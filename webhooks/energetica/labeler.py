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
    request.app.loop.create_task(asign_energetica_label(request.app, request.json))

    return response.json({}, status=200)


async def asign_energetica_label(app, body):
    logger.info('Energetica labeler task triggered')
    energetica_emails = app.dbUtils.get_energetica_emails()
    if body.get('primaryCustomer', {}).get('email', '') in energetica_emails:
        msg = 'Moving conversation [%s] from [%s] to Energetica mailbox'
        logger.info(msg, body.get('subject'), body['primaryCustomer']['email'])

        mailbox_id = await app.hsApi.get_mailbox('Energética Coop')
        await app.hsApi.change_mailbox(body['id'], mailbox_id['id'])

    logger.info('Energetica labeler task ended')
