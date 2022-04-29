from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email')

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user
