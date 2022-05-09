from functools import reduce

from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .mixins import ListModelMixin

from ..serializers import MessageSerializer, SearchSerializer
from ..models import Message


class MessageViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Message.objects.none()
        # only allow authenticated users to view their own details
        return Message.objects.filter(account_id__user=self.request.user)\
            .select_related('folder')\
            .prefetch_related('messageparticipant_set__participant')\
            .order_by('date')


class SearchMessageView(APIView):

    @swagger_auto_schema(
        operation_id='search_message',
        request_body=SearchSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = SearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        queryset = Message.objects.filter(account_id__user=self.request.user)

        from_ = serializer.data.get('from_', [])
        if from_:
            queryset = queryset.filter(
                messageparticipant__participant__email__in=from_,
                messageparticipant__type='from',
            )

        to = serializer.data.get('to', [])
        if to:
            queryset = queryset.filter(
                messageparticipant__participant__email__in=to,
                messageparticipant__type='to',
            )

        subject = serializer.data.get('subject', None)
        if subject:
            queryset = queryset.filter(
                subject__icontains=subject,
            )

        body = serializer.data.get('body', None)
        if body:
            queryset = queryset.filter(
                body__icontains=body,
            )

        from_date = serializer.data.get('from_date', None)
        if from_date:
            queryset = queryset.filter(
                date__gte=from_date,
            )

        to_date = serializer.data.get('to_date', None)
        if to_date:
            queryset = queryset.filter(
                date__lte=to_date,
            )

        labels = serializer.data.get('labels', [])
        if labels:
            # check for partial matches with any of the labels
            queryset = queryset.filter(
                reduce(lambda a, b: a | b, [
                    Q(thread__labels__display_name__icontains=label) for label in labels
                ])
            )

        starred = serializer.data.get('starred', None)
        if starred is not None:
            queryset = queryset.filter(starred=starred)

        unread = serializer.data.get('unread', None)
        if unread is not None:
            queryset = queryset.filter(unread=unread)

        queryset = queryset.distinct()

        result_serializer = MessageSerializer(queryset, many=True)
        return Response(result_serializer.data)
