from getpass import getpass
from django.core.management.base import BaseCommand, CommandError
from user.models import User

"""
python manage.py resetadminpassword
"""

# python getpass module is used to hide the password input from the user in the console.


class Command(BaseCommand):
    help = 'resets the default admin password'

    def handle(self, *args, **options):
        try:
            user = User.objects.get(is_superuser=True)
        except User.DoesNotExist:
            raise CommandError('No admin user found.')
        except User.MultipleObjectsReturned:
            # this should never happen; but just in case
            raise CommandError('Multiple admin users found.')
        else:
            password = getpass('Enter new password: ')
            password_confirm = getpass('Confirm new password: ')
            if password != password_confirm:
                raise CommandError('Passwords do not match.')
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS('Password reset successful.'))
