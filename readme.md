### installation

1. add the `.env` file to project root
2. `pip install -r requirements.txt`
3. `docker-compose up -d` for database and redis
4. `python manage.py migrate`
5. `python manage.py runserver`
6. `celery -A userManagementWithEmailInteration beat -l INFO` for background tasks beats
7. `celery -A userManagementWithEmailInteration worker -l INFO` for background tasks worker
8. open `http://localhost:8000/swagger/`

**Please create a superuser using `python manage.py createsuperuser`**


### webhooks
1. Link local app to the internet using **ngrok**.
2. Place the `<ngrock_url>/webhooks/` in your webhook url in nylas application.
3. Done.
4. To test, open, create, or reply to a mail linked in nylas application.