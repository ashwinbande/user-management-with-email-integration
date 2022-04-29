from django.urls import path

from .views import UserCreateAPIView


urlpatterns = [
    path('user-create', UserCreateAPIView.as_view(), name='user-create'),
]