from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

"""
Nylas Api Schema for Account:
{
  "id": "awa6ltos76vz5hvphkp8k17nt",
  "object": "account",
  "account_id": "awa6ltos76vz5hvphkp8k17nt",
  "name": "Dorothy Vaughan",
  "provider": "gmail",
  "organization_unit": "label",
  "sync_state": "running",
  "linked_at": 1470231381,
  "email_address": "dorothy@spacetech.com",
  "metadata": {
    "your-key": "string"
  }
}
"""


class NylasUserAccount(models.Model):
    organization_unit_choices = (
        ('label', 'Label'),
        ('folder', 'Folder'),
    )

    sync_state_choices = (
        ('running', 'Running'),
        ('stopped', 'Stopped'),
        ('invalid', 'Invalid'),
    )

    id = models.CharField(max_length=100, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    provider = models.CharField(max_length=100)
    organization_unit = models.CharField(max_length=10, choices=organization_unit_choices)
    sync_state = models.CharField(max_length=10, choices=sync_state_choices)
    linked_at = models.DateTimeField()

    @property
    def email_address(self):
        return self.user.email

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Nylas User Account'


class NylasUserChildMixin(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    account_id = models.ForeignKey(NylasUserAccount, on_delete=models.CASCADE)

    class Meta:
        abstract = True
