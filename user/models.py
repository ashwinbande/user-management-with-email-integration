from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, validators=[UnicodeUsernameValidator()])
    email = models.EmailField()
    is_active = models.BooleanField(default=True)

    # region things specific to Custom User Model
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    # endregion

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def save(self, *args, **kwargs):
        """
        Checks if only one admin user exists in the database.
        """
        if self.is_superuser and User.objects.filter(is_superuser=True).exclude(pk=self.pk).exists():
            raise ValueError('An Admin User already exists.')
        return super().save(*args, **kwargs)

    # region is_staff
    # the 'is_staff' field is required by the Django admin, but we don't want to use it,
    # so we override it and set it to False
    @property
    def is_staff(self):
        return self.is_superuser

    @is_staff.setter
    def is_staff(self, value):
        pass
    # endregion

