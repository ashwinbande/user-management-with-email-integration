from django.db import models
from django.utils.functional import cached_property

from .user_account import NylasUserChildMixin
from .folder import Folder
from .label import Label
from .participant import Participant


class Thread(NylasUserChildMixin):
    first_message_timestamp = models.IntegerField(null=True)
    folders = models.ManyToManyField(Folder, related_name='threads')
    has_attachments = models.BooleanField(default=False)

    last_message_received_timestamp = models.IntegerField(null=True)
    last_message_sent_timestamp = models.IntegerField(null=True)
    last_message_timestamp = models.IntegerField(null=True)

    # participants = models.ManyToManyField('Participant', related_name='threads')
    # snippet = models.CharField(max_length=500)

    starred = models.BooleanField(default=False)
    subject = models.CharField(max_length=500)

    unread = models.BooleanField(default=True)
    version = models.IntegerField(default=0)

    labels = models.ManyToManyField(Label, related_name='threads')

    # draft_ids = None -- deliberately omitted
    # message_ids = None -- deliberately omitted

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Thread'

    @cached_property
    def participants(self):
        return Participant.objects.filter(messageparticipant__message__thread_id=self).distinct()

    @cached_property
    def snippet(self):
        last_message = self.message_set.order_by('date').last()
        return last_message.snippet if last_message else ''
