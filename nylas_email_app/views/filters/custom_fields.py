from django_filters.constants import EMPTY_VALUES
from django_filters.rest_framework import BaseInFilter, CharFilter, Filter


class AdditionalFilterMixin(Filter):
    """
    Mixin to add additional filters to the queryset
    in the form of additional_filter_args and additional_filter_kwargs
    the additional_filter_args should return a tuple, like: Q objects
    the additional_filter_kwargs should return a dict, like: {'key': value}
    """

    def __init__(self, *args, **kwargs):
        self.additional_filter_args = kwargs.pop('additional_filter_args', ())
        self.additional_filter_kwargs = kwargs.pop('additional_filter_kwargs', {})
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs
        if self.distinct:
            qs = qs.distinct()
        lookup = '%s__%s' % (self.field_name, self.lookup_expr)
        qs = self.get_method(qs)(*self.additional_filter_args, **self.additional_filter_kwargs, **{lookup: value})
        return qs


class ListFilter(BaseInFilter, CharFilter, AdditionalFilterMixin):
    pass
