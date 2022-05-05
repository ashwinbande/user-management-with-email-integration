from datetime import timedelta
from time import mktime
from celery import shared_task
from decouple import config
from django.db import transaction
from django.utils import timezone
from nylas import APIClient
from rest_framework.exceptions import ValidationError

from ..models import (
    NylasUserAccount, Thread, Folder, Label, Message, Participant,
    MessageParticipant,
)


def create_message_participant(message_instance, data: dict, participant_type):
    participant, _ = Participant.objects.get_or_create(
        email=data.get('email'), defaults={'name': data.get('name')}
    )
    MessageParticipant.objects.create(
        message=message_instance,
        participant=participant,
        type=participant_type,
    )


def save_message_by_id(message_id, thread_instance: Thread, nylas):
    """
    message.id
    message.account_id
    message.body
    message.date
    message.folder
    message.snippet
    message.starred
    message.subject
    message.thread_id
    message.unread
    message.bcc
    message.cc
    message.from_
    message.to

    message.object
    message.files
    message.events
    message.labels
    message.received_at
    """
    message = nylas.messages.get(message_id)
    # get or create folder if it exists in message
    if hasattr(message, 'folder') and message.folder:
        message_folder, _ = Folder.objects.get_or_create(
            id=message.folder.id,
            name=message.folder.name,
            account_id=thread_instance.account_id,
            defaults={
                'display_name': message.folder.display_name,
            })
    else:
        message_folder = None

    # save message instance
    message_instance, created = Message.objects.update_or_create(
        id=message.id,
        account_id=thread_instance.account_id,
        defaults=dict(
            body=message.body,
            date=message.date,
            folder=message_folder,
            snippet=message.snippet,
            starred=message.starred,
            subject=message.subject,
            thread_id=thread_instance,
            unread=message.unread,
            reply_to_message_id=message.reply_to_message_id,
        )
    )
    # participant should not change in message; hence only create them if message is created
    if created:
        # create bcc participants
        for bcc in message.bcc:
            create_message_participant(message_instance, bcc, 'bcc')
        # create cc participants
        for cc in message.cc:
            create_message_participant(message_instance, cc, 'cc')
        # create from participants
        for from_ in message.from_:
            create_message_participant(message_instance, from_, 'from')
        # create reply_to participants
        for reply_to in message.reply_to:
            create_message_participant(message_instance, reply_to, 'reply_to')
        # create to participants
        for to in message.to:
            create_message_participant(message_instance, to, 'to')


def save_thread_with_messages(thread, user: NylasUserAccount, nylas):
    """
    thread.id
    thread.account_id
    thread.first_message_timestamp
    thread.has_attachments
    thread.last_message_received_timestamp
    thread.last_message_timestamp
    thread.starred
    thread.subject
    thread.unread
    thread.version

    thread.message_ids
    thread.labels # Gmail accounts only
    thread.folders # All providers other than Gmail

    ### not implemented:
    thread.object
    thread.first_message_at
    thread.snippet
    thread.participants
    thread.draft_ids
    thread.last_message_received_at
    thread.last_message_at
    """
    # save thread instance
    thread_instance, created = Thread.objects.update_or_create(
        id=thread.id, account_id=user,
        defaults=dict(
            first_message_timestamp=thread.first_message_timestamp,
            has_attachments=thread.has_attachments,
            last_message_received_timestamp=thread.last_message_received_timestamp,
            last_message_sent_timestamp=thread.last_message_sent_timestamp,
            last_message_timestamp=thread.last_message_timestamp,
            starred=thread.starred,
            subject=thread.subject,
            unread=thread.unread,
            version=thread.version,
        )
    )
    # add many-to-many relationship between thread and folder
    thread_instance.folders.clear()
    for folder in thread.folders:
        # create folder instance if it doesn't exist
        thread_folder, _ = Folder.objects.get_or_create(
            id=folder.id, name=folder.name, account_id=user,
            defaults={'display_name': folder.display_name}
        )
        thread_instance.folders.add(thread_folder)

    # add many-to-many relationship between thread and label
    thread_instance.labels.clear()
    for label in thread.labels:
        # create label instance if it doesn't exist
        thread_label, _ = Label.objects.get_or_create(
            id=label.id, name=label.name, account_id=user,
            defaults={'display_name': label.display_name}
        )
        thread_instance.labels.add(thread_label)

    # save messages associated with thread
    for message_id in thread.message_ids:
        save_message_by_id(message_id, thread_instance, nylas)


@shared_task
def sync_nylas_for_user(user_id: str):
    try:
        user = NylasUserAccount.objects.get(id=user_id)
    except NylasUserAccount.DoesNotExist:
        raise ValidationError('User does not exist')

    try:
        nylas = APIClient(
            config('NYLAS_CLIENT_ID'),
            config('NYLAS_CLIENT_SECRET'),
            user.access_token,
        )
    except Exception as e:
        raise ValidationError(detail=e)
    else:
        # for thread in nylas.threads.all():
        sync_after_datetime = timezone.now() - timedelta(days=config('LAST_N_DAYS_SYNC', cast=int))
        after_timestamp = int(mktime(sync_after_datetime.timetuple()))
        for thread in nylas.threads.where(started_after=after_timestamp):
            # saving with atomic transaction so
            # the overhead of saving is minimal
            with transaction.atomic():
                save_thread_with_messages(thread, user, nylas)
