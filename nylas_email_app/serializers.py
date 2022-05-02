from rest_framework.serializers import ModelSerializer
from .models import UserNylasDetail


class UserNylasDetailSerializer(ModelSerializer):

    class Meta:
        model = UserNylasDetail
        fields = '__all__'
