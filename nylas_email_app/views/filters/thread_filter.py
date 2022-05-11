from django_filters.rest_framework import FilterSet, CharFilter, NumberFilter, BooleanFilter
from ...models import Thread

from .custom_fields import ListFilter


class ThreadFilter(FilterSet):
    from_ = ListFilter(
        field_name='message__messageparticipant__participant__email',
        additional_filter_kwargs=dict(message__messageparticipant__type='from'),
        distinct=True,
    )
    to = ListFilter(
        field_name='message__messageparticipant__participant__email',
        additional_filter_kwargs=dict(message__messageparticipant__type='to'),
        distinct=True,
    )
    subject = CharFilter(field_name='subject', lookup_expr='icontains', distinct=True)
    body = CharFilter(field_name='message__body', lookup_expr='icontains', distinct=True)
    from_date = NumberFilter(
        field_name='first_message_timestamp', lookup_expr='gte', distinct=True
    )
    to_date = NumberFilter(
        field_name='last_message_timestamp', lookup_expr='lte', distinct=True
    )
    labels = ListFilter(field_name='labels__display_name', distinct=True)
    starred = BooleanFilter(field_name='starred', distinct=True)
    unread = BooleanFilter(field_name='unread', distinct=True)

    class Meta:
        model = Thread
        fields = [
            'from_', 'to', 'subject', 'body', 'from_date', 'to_date',
            'labels', 'starred', 'unread',
        ]
