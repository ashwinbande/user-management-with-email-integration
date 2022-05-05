from django.urls import path

from .views import NylasUserAccountViewSet


urlpatterns = [
    path('register-credentials', NylasUserAccountViewSet.as_view({'post': 'create'}), name='create-user'),
    path('modify-credentials/<int:pk>', NylasUserAccountViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'delete': 'destroy'
    }), name='modify-user'),
    # path('list-emails', NylasListEmailView.as_view(), name='list-emails'),
]
