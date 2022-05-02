from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from nylas import APIClient

from .serializers import UserNylasDetailSerializer
from .models import UserNylasDetail


class NylasUserDetailViewSet(ModelViewSet):
    serializer_class = UserNylasDetailSerializer

    def get_queryset(self):
        # only allow authenticated users to view their own details
        return UserNylasDetail.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        raise PermissionDenied(detail='Cant List User Details')


class NylasListEmailView(APIView):

    def get(self, request, *args, **kwargs):
        try:
            user_nylas_detail = UserNylasDetail.objects.get(user=request.user)
        except UserNylasDetail.DoesNotExist:
            return Response(data={'detail': 'User Nylas Detail Does Not Exist'}, status=404)

        nylas = APIClient(
            user_nylas_detail.nylas_client_id,
            user_nylas_detail.nylas_client_secret,
            user_nylas_detail.nylas_access_token,
        )

        # message = nylas.messages.first()
        # d = f'Subject: {message.subject} | Unread: {message.unread} | from: {message.from_} | ID: {message.id}'

        threads = nylas.threads.all(limit=10)

        list_of_threads = [f'Subject: {thread.subject} | Participants: {thread.participants}' for thread in threads]

        return Response(data=list_of_threads, status=200)