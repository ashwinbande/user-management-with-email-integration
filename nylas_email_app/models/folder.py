from django.db import models
from .user_account import NylasUserChildMixin


"""
Nylas API schema for Folder
{
  "account_id": "79xcak1h10r1tmm5ogavx28lb",
  "display_name": "Archive",
  "id": "ajs4ef7xu74vns6o5ufsu69m7",
  "name": "archive",
  "object": "folder"
}
"""


class Folder(NylasUserChildMixin):
    name = models.CharField(max_length=100)
    display_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Folder'
