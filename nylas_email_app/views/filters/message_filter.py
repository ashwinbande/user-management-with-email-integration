from django_filters.rest_framework import FilterSet, CharFilter, NumberFilter, BooleanFilter
from ...models import Message

from .custom_fields import ListFilter


class MessageFilter(FilterSet):
    from_ = ListFilter(
        field_name='messageparticipant__participant__email',
        additional_filter_kwargs=dict(messageparticipant__type='from'),
        distinct=True,
    )
    to = ListFilter(
        field_name='messageparticipant__participant__email',
        additional_filter_kwargs=dict(messageparticipant__type='to'),
        distinct=True,
    )
    subject = CharFilter(field_name='subject', lookup_expr='icontains', distinct=True)
    body = CharFilter(field_name='body', lookup_expr='icontains', distinct=True)
    from_date = NumberFilter(field_name='date', lookup_expr='gte', distinct=True)
    to_date = NumberFilter(field_name='date', lookup_expr='lte', distinct=True)
    labels = ListFilter(field_name='thread__labels__display_name', distinct=True)
    starred = BooleanFilter(field_name='starred', distinct=True)
    unread = BooleanFilter(field_name='unread', distinct=True)

    class Meta:
        model = Message
        fields = [
            'from_', 'to', 'subject', 'body', 'from_date', 'to_date',
            'labels', 'starred', 'unread',
        ]
