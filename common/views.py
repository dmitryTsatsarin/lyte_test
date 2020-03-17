from django.http import HttpResponse
from django.utils.functional import cached_property
from rest_framework import status as rest_status
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import JSONRenderer

from common.serializers import EmptySerializer


class JsonResponse(HttpResponse):
    def __init__(self, data=None, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json; charset=utf-8'
        super().__init__(content, **kwargs)


class CommonGenericView(GenericAPIView):
    serializer_class = EmptySerializer
    lookup_field = 'id'
    serializer_class_receive = None
    serializer_class_response = None
    serializer_class_query = None

    @cached_property
    def query_params_data(self):
        return self.get_query_data()

    def get_query_data(self):
        serializer = self.get_query_serializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def get_query_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        assert self.serializer_class_query is not None, (
                "'%s' should either include a `serializer_class_query` attribute, "
                "or override the `get_query_serializer_class()` method."
                % self.__class__.__name__)

        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class_query(*args, **kwargs)

    def perform_update(self, serializer, **kwargs):
        serializer.save(**kwargs)

    def update_raw(self, request, *args, **kwargs):
        instance = self.get_object()

        partial = kwargs.pop('partial', False)
        if self.serializer_class_receive:
            self.serializer_class = self.serializer_class_receive
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, **kwargs)
        instance.refresh_from_db()
        if self.serializer_class_response:
            self.serializer_class = self.serializer_class_response
        serializer = self.get_serializer(instance)
        data = serializer.data
        return data

    def update(self, request, *args, **kwargs):
        data = self.update_raw(request, *args, **kwargs)
        return JsonResponse(data)

    def list(self, request, *args, **kwargs):
        data = self.list_raw(request, *args, **kwargs)
        if self._paginated:
            return self.get_paginated_response(data)
        return JsonResponse(data)

    def list_raw(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        self._paginated = False
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            self._paginated = True
        else:
            serializer = self.get_serializer(queryset, many=True)
        return serializer.data
