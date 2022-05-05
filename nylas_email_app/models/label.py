from django.db import models
from .user_account import NylasUserChildMixin


"""
Nylas API schema for Label:
{
  "account_id": "{account_id}",
  "display_name": "label",
  "id": "{label_id}",
  "name": "inbox",
  "object": "label"
}
"""


class Label(NylasUserChildMixin):
    name = models.CharField(max_length=100, blank=True, null=True)
    display_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Label'
