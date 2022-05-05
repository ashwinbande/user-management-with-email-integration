from django.db.models.signals import post_save
from django.dispatch import receiver

from .tasks import sync_nylas_for_user
from .models import NylasUserAccount


@receiver(post_save, sender=NylasUserAccount)
def sync_threads(sender, instance, created, **kwargs):
    if created:
        sync_nylas_for_user.delay(instance.id)
