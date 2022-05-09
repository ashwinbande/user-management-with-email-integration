from rest_framework.response import Response


class ListModelMixin:
    """
    Modified ListModelMixin to add list_mode=True in serializer context
    """

    def get_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        kwargs['context']['list_mode'] = kwargs.pop('list_mode', False)
        return serializer_class(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, list_mode=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, list_mode=True)
        return Response(serializer.data)