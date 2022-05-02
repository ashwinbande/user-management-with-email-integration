from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class UserNylasDetail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nylas_client_id = models.CharField(max_length=100)
    nylas_client_secret = models.CharField(max_length=100)
    nylas_access_token = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'User Nylas Detail'
