# Generated by Django 4.0.4 on 2022-05-05 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nylas_email_app', '0002_folder_label_message_messageparticipant_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='reply_to_message_id',
            field=models.CharField(default=None, max_length=500, null=True),
        ),
    ]
