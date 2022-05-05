from decouple import config
from nylas import APIClient

from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError
from .models import NylasUserAccount


class NylasUserAccountSerializer(ModelSerializer):

    class Meta:
        model = NylasUserAccount
        fields = ('user', 'access_token')

    def create(self, validated_data):
        user = validated_data.get('user')
        access_token = validated_data.get('access_token')
        try:
            nylas = APIClient(
                config('NYLAS_CLIENT_ID'),
                config('NYLAS_CLIENT_SECRET'),
                access_token,
            )
        except Exception as e:
            raise ValidationError(detail=e)
        else:
            account = nylas.account
            return NylasUserAccount.objects.create(
                id=account.id,
                user=user,
                access_token=access_token,
                name=account.name,
                provider=account.provider,
                organization_unit=account.organization_unit,
                sync_state=account.sync_state,
                linked_at=account.linked_at,
            )

    def update(self, instance, validated_data):
        instance.access_token = validated_data.get('access_token')
        instance.save()
        return instance
