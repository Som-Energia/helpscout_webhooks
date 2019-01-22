import base64
import hmac
import logging

from sanic import Blueprint
from sanic import response

from ..lib.hs_api import HelpscoutSDK
from ..lib.utils import dbUtils

from webhooks.conf import settings


logger = logging.getLogger('energetica')

labeler = Blueprint("energetica_labeler", url_prefix="/energetica_labeler")

db = dbUtils()


@labeler.middleware('request')
async def check_signature(request):

    request_signature = base64.encodebytes(hmac.new(
        settings.SECRET_KEY.encode(),
        request.body,
        'sha1'
    ).digest()).strip().decode()

    hs_signature = request.headers['x-helpscout-signature']

    if request_signature != hs_signature:
        return response.json({'error': 'Unauthorized'}, status=401)


@labeler.route("/", methods=['POST'])
async def labelhook(request):
    hsApi = HelpscoutSDK()

    body = request.json
    if body['createdBy']['email'] in db.energeticaMails():
        # Patch method
        logger.debug('-' * 10 + 'ENERGETICA' + '-' * 10)
        mailbox_id = await hsApi.get_mailbox('GDPR')
        logger.debug(mailbox_id)

    logger.debug('yujuuuuu')

    return response.json({}, status=200)
