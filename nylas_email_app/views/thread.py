from functools import reduce

from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from django_filters import rest_framework as filters

from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.filters import SearchFilter

from .mixins import ListModelMixin

from ..serializers import ThreadSerializer, SearchSerializer
from ..models import Thread

from .filters import ThreadFilter


class ThreadViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    serializer_class = ThreadSerializer
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filter_class = ThreadFilter
    search_fields = ('subject', 'message__snippet')

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Thread.objects.none()
        # only allow authenticated users to view their own details
        return Thread.objects.filter(account_id__user=self.request.user)\
            .prefetch_related('message_set', 'folders', 'labels')\
            .order_by('last_message_received_timestamp')


class SearchThreadView(APIView):

    @swagger_auto_schema(
        operation_id='search_thread',
        request_body=SearchSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = SearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        queryset = Thread.objects.filter(account_id__user=self.request.user)

        from_ = serializer.data.get('from_', [])
        if from_:
            queryset = queryset.filter(
                message__messageparticipant__participant__email__in=from_,
                message__messageparticipant__type='from',
            )

        to = serializer.data.get('to', [])
        if to:
            queryset = queryset.filter(
                message__messageparticipant__participant__email__in=to,
                message__messageparticipant__type='to',
            )

        subject = serializer.data.get('subject', None)
        if subject:
            queryset = queryset.filter(
                subject__icontains=subject,
            )

        body = serializer.data.get('body', None)
        if body:
            queryset = queryset.filter(
                message__body__icontains=body,
            )

        from_date = serializer.data.get('from_date', None)
        if from_date:
            queryset = queryset.filter(
                first_message_received_timestamp__gte=from_date,
            )

        to_date = serializer.data.get('to_date', None)
        if to_date:
            queryset = queryset.filter(
                last_message_received_timestamp__lte=to_date,
            )

        labels = serializer.data.get('labels', [])
        if labels:
            # check for partial matches with any of the labels
            queryset = queryset.filter(
                reduce(lambda a, b: a | b, [
                    Q(labels__display_name__icontains=label) for label in labels
                ])
            )

        starred = serializer.data.get('starred', None)
        if starred is not None:
            queryset = queryset.filter(starred=starred)

        unread = serializer.data.get('unread', None)
        if unread is not None:
            queryset = queryset.filter(unread=unread)

        queryset = queryset.distinct()

        result_serializer = ThreadSerializer(queryset, many=True)
        return Response(result_serializer.data)