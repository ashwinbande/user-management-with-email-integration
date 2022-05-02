from django.urls import path

from .views import NylasUserDetailViewSet, NylasListEmailView


urlpatterns = [
    path('register-credentials', NylasUserDetailViewSet.as_view({'post': 'create'}), name='create-user'),
    path('modify-credentials/<int:pk>', NylasUserDetailViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'delete': 'destroy'
    }), name='modify-user'),
    path('list-emails', NylasListEmailView.as_view(), name='list-emails'),
]
