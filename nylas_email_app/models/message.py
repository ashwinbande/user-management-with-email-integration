from django.db import models
from django.utils.functional import cached_property

from .user_account import NylasUserChildMixin
from .folder import Folder
from .label import Label
from .thread import Thread
from .participant import Participant


class Message(NylasUserChildMixin):
    body = models.TextField()

    date = models.IntegerField()

    # event = None --deliberately omitted
    # files = None --deliberately omitted
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, default=None)

    snippet = models.CharField(max_length=500)
    starred = models.BooleanField(default=False)
    subject = models.CharField(max_length=500)

    thread_id = models.ForeignKey(Thread, on_delete=models.CASCADE, null=True, default=None)

    unread = models.BooleanField(default=True)
    # labels = models.ManyToManyField(Label, related_name='messages')

    # saving as string because foreignkey requires that object tobe created first
    # might be able to correct this in the future
    reply_to_message_id = models.CharField(max_length=500, null=True, default=None)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Message'

    @property
    def base_participants(self):
        return self.messageparticipant_set.select_related('participant').all()

    @cached_property
    def bcc(self):
        return self.base_participants.filter(type='bcc')

    @cached_property
    def cc(self):
        return self.base_participants.filter(type='cc')

    @cached_property
    def from_(self):
        return self.base_participants.filter(type='from')

    @cached_property
    def reply_to(self):
        return self.base_participants.filter(type='reply_to')

    @cached_property
    def to(self):
        return self.base_participants.filter(type='to')


class MessageParticipant(models.Model):
    participant_type_choices = (
        ('reply_to', 'Reply To'),
        ('to', 'To'),
        ('from', 'From'),
        ('cc', 'Cc'),
        ('bcc', 'Bcc'),
    )
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=participant_type_choices)

    def __str__(self):
        return f'{self.message.subject} - {self.participant.name}'

    class Meta:
        verbose_name = 'Message Participant'
        # unique_together = ('message', 'participant')
