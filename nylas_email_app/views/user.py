from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet

from ..serializers import NylasUserAccountSerializer
from..models import NylasUserAccount


class NylasUserAccountViewSet(ModelViewSet):
    serializer_class = NylasUserAccountSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return NylasUserAccount.objects.none()
        # only allow authenticated users to view their own details
        return NylasUserAccount.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        raise PermissionDenied(detail='Cant List User Details')