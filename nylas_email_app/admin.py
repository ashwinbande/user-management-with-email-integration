from django.contrib import admin
from .models import (
    NylasUserAccount, Folder, Label, Thread, Participant, Message,
)

admin.site.register(NylasUserAccount)
admin.site.register(Folder)
admin.site.register(Label)
admin.site.register(Thread)
admin.site.register(Participant)
admin.site.register(Message)
