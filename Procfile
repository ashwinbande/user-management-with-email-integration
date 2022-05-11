web: gunicorn userManagementWithEmailInteration.wsgi
worker: celery -A userManagementWithEmailInteration worker -l INFO
beat: celery -A userManagementWithEmailInteration beat -l INFO
