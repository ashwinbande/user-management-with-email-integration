from django.db import models


class Participant(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, primary_key=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Participant'
