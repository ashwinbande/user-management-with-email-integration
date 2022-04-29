from django.contrib.auth import get_user_model

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from .permissions import IsAdmin
from .serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # modified data contains password string
        modified_data = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(modified_data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        # create random password as per requirements and set is_superuser to False
        random_password = get_user_model().objects.make_random_password()
        serializer.save(is_superuser=False, password=random_password)
        # serializer can't return string password, so we need to set it in the data
        modified_data = dict(serializer.data)
        modified_data['password'] = random_password
        return modified_data
