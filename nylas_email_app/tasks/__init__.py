from celery import shared_task, group
from decouple import config
from nylas import APIClient
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from .sync_nylas_for_user import sync_nylas_for_user

__all__ = [
    'sync_nylas_for_user',
]

# User = get_user_model()
#
#
# @shared_task
# def load_new_messages_for_user(user):
#     print('load_new_messages_if_sync_completed')
#
#
# @shared_task(name='load_new_messages_if_sync_completed')
# def load_new_messages_if_sync_completed():
#     print('load new messages if sync completed for each user')
#     g = group(load_new_messages_for_user.s(user) for user in User.objects.all() if user.sync_complete)
#     g.apply_async()
#
#
# @shared_task()
# def sync_nylas_messages_for_user(user):
#     print('sync nylas messages for user: ', user)
#
#
# @shared_task(name='sync_nylas_messages')
# def sync_nylas_messages():
#     print('sync nylas messages for each user')
#     """
#     for user in User.objects.all():
#         if not user.sync_complete:
#             sync_nylas_messages_for_user.delay(user)
#     """
#
#     g = group(sync_nylas_messages_for_user.s(user) for user in User.objects.all() if not user.sync_complete)
#     g.apply_async()
#
#
