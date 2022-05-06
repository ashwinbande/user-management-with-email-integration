from decouple import config
from nylas import APIClient

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.exceptions import ValidationError
from .models import (
    NylasUserAccount, Thread, Message, MessageParticipant,
    Label, Folder, Participant,
)


class ListOperationsMixin(ModelSerializer):

    exclude_in_list = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        list_mode = kwargs.get('context', {}).get('list_mode', False)

        # remove fields from exclude_in_list if list_mode is True
        if list_mode:
            for field_name in self.exclude_in_list:
                self.fields.pop(field_name)


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


class FolderSerializer(ModelSerializer):

    class Meta:
        model = Folder
        exclude = ('id', 'account_id')


class LabelSerializer(ModelSerializer):
    class Meta:
        model = Label
        exclude = ('id', 'account_id')


class MessageParticipantSerializer(ModelSerializer):

    class Meta:
        model = MessageParticipant
        exclude = ('message', 'id')


class MessageSerializer(ListOperationsMixin, ModelSerializer):
    messageparticipant_set = MessageParticipantSerializer(many=True)
    folder = FolderSerializer()
    labels = LabelSerializer(many=True)

    exclude_in_list = ('messageparticipant_set', 'folder', 'body')

    class Meta:
        model = Message
        fields = '__all__'


class ParticipantSerializer(ModelSerializer):

    class Meta:
        model = Participant
        fields = '__all__'


class ThreadSerializer(ListOperationsMixin, ModelSerializer):
    message_set = MessageSerializer(many=True)
    labels = LabelSerializer(many=True)
    folders = FolderSerializer(many=True)

    participants = ParticipantSerializer(many=True)
    snippet = serializers.ReadOnlyField()

    exclude_in_list = ('message_set', 'labels', 'folders', 'participants')

    class Meta:
        model = Thread
        fields = '__all__'


class SearchSerializer(Serializer):
    from_ = serializers.ListField(child=serializers.EmailField(), required=False)
    to = serializers.ListField(child=serializers.EmailField(), required=False)
    subject = serializers.CharField(required=False)
    body = serializers.CharField(required=False)
    from_date = serializers.IntegerField(required=False)
    to_date = serializers.IntegerField(required=False)
    labels = serializers.ListField(child=serializers.CharField(), required=False)
    starred = serializers.BooleanField(required=False)
    unread = serializers.BooleanField(required=False)