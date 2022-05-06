import os
from datetime import timedelta
from celery import Celery
from decouple import config

# Set the default Django settings module for the 'celery' program.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'userManagementWithEmailInteration.settings')

app = Celery('userManagementWithEmailInteration')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    """
    #Scheduler Name
    'print-message-ten-seconds': {
        # Task Name (Name Specified in Decorator)
        'task': 'print_msg_main',  
        # Schedule      
        'schedule': 10.0,  # or timedelta(minutes=15),
        # Function Arguments 
        'args': ("Hello",) ,
        'kwargs': {'message': 'Hello'},
    },
    """
    're-sync-messages-for-all-users': {
        'task': 're_sync_messages_for_all_users',
        'schedule': timedelta(minutes=config('PERIODIC_SYNC_IN_MINUTES', cast=int)),
        'args': (),
        'kwargs': {},
    }
}
