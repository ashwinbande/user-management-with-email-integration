from django.urls import path, include

from .views import (
    NylasUserAccountViewSet, ThreadViewSet, MessageViewSet,
    SearchThreadView, SearchMessageView,
)


thread_urls = [
    path('threads', ThreadViewSet.as_view({'get': 'list'}), name='thread-list'),
    path('threads/search', SearchThreadView.as_view(), name='thread-search'),
    path('thread/<str:pk>', ThreadViewSet.as_view({'get': 'retrieve'}), name='thread-detail'),
]

message_urls = [
    path('messages', MessageViewSet.as_view({'get': 'list'}), name='message-list'),
    path('messages/search', SearchMessageView.as_view(), name='message-search'),
    path('message/<str:pk>', MessageViewSet.as_view({'get': 'retrieve'}), name='message-detail'),
]

urlpatterns = [
    path('register-credentials', NylasUserAccountViewSet.as_view({'post': 'create'}), name='create-user'),
    path('modify-credentials/<int:pk>', NylasUserAccountViewSet.as_view({
        'get': 'retrieve', 'put': 'update', 'delete': 'destroy'
    }), name='modify-user'),
    path('email/', include(thread_urls + message_urls)),
]
