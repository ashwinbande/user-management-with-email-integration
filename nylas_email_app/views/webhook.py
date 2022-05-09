import hashlib
import hmac

from decouple import config
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from ..tasks import update_thread_from_webhook_delta


def verify_signature(message, key, signature):
    """
    This function will verify the authenticity of a digital signature.
    For security purposes, Nylas includes a digital signature in the headers
    of every webhook notification, so that clients can verify that the
    webhook request came from Nylas and no one else. The signing key
    is your OAuth client secret, which only you and Nylas know.
    """
    try:
        digest = hmac.new(key, msg=message, digestmod=hashlib.sha256).hexdigest()
        return hmac.compare_digest(digest, signature)
    except Exception as e:
        print(e)
        return False


class NylasWebhookView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        challenge = request.query_params.get('challenge', None)
        return HttpResponse(content=challenge, status=200)

    def post(self, request, *args, **kwargs):
        genuine = verify_signature(
            message=request.body,
            key=config('NYLAS_CLIENT_SECRET', cast=str).encode("utf8"),
            signature=request.META.get('HTTP_X_NYLAS_SIGNATURE', None),
        )
        if not genuine:
            return HttpResponse(content='Signature verification failed!', status=401)
        # process deltas
        deltas = request.data.get('deltas', [])
        for delta in deltas:
            account_id = delta.get('object_data', {}).get('account_id', None)
            thread_id = delta.get('object_data', {}).get('attributes', {}).get('thread_id', None)
            update_thread_from_webhook_delta.delay(account_id, thread_id)
        return HttpResponse(content='Deltas have been queued', status=200)
