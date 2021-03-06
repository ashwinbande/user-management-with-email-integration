from celery import shared_task

from .sync_nylas_for_user import sync_nylas_for_user, update_thread_from_webhook_delta

from ..models import NylasUserAccount

__all__ = [
    'sync_nylas_for_user',
    'update_thread_from_webhook_delta',
]


@shared_task(name='re_sync_messages_for_all_users')
def re_sync_messages_for_all_users():
    for user in NylasUserAccount.objects.all():
        sync_nylas_for_user.delay(user.id, resync=True)
