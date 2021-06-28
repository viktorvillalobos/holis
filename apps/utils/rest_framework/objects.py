from typing import Dict, Optional, Union

from django.utils.functional import cached_property
from rest_framework.response import Response
from rest_framework.views import APIView

from collections.abc import Callable, Iterator
from copy import deepcopy

from .paginators import CursoredAPIPagination


class PaginationAPIViewMixin:
    pagination_class = None
    pagination_class_config: Dict = None
    page_size: int = 10

    def get_pagination_class(self):
        return self.pagination_class

    def get_pagination_class_context(self) -> Dict:
        context = deepcopy(self.pagination_class_config) or {}
        context.update(
            {
                "request": getattr(self, "request"),
                "view": self,
                "page_size": self.page_size,
            }
        )
        return context

    @cached_property
    def paginator(self):
        pagination_class = self.get_pagination_class()
        return pagination_class(**self.get_pagination_class_context())

    def paginate(self, *args, **kwargs):
        return self.paginator.paginate(*args, **kwargs)

    def get_paginated_response(self, page):
        return self.paginator.get_paginated_response(page)


class SerializationAPIViewMixin:
    serializer_class = None

    def get_serializer_class(self):
        return self.serializer_class

    def get_serializer_context(self):
        return {
            "request": getattr(self, "request"),
            "format": getattr(self, "format_kwarg"),
            "view": self,
        }

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()

        if serializer_class is None:
            return None

        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)


class GenericObjectAPIView(PaginationAPIViewMixin, SerializationAPIViewMixin, APIView):
    #: generator can be a generator function, an Iterator, a Generator or anything that returns an iterable
    objects_generator: Union[Callable, Iterator] = None
    pagination_class = CursoredAPIPagination

    def get_object(self):
        raise NotImplementedError

    def get_objects_generator(self):
        return self.objects_generator

    def get_objects_generator_context(self) -> Optional[Dict]:
        return None

    def paginate_objects_generator(self, objects_generator):
        objects_generator_context = self.get_objects_generator_context()
        return self.paginator.paginate(
            objects_generator, extra_context=objects_generator_context
        )


class ListObjectMixin:
    def list(self, request, *args, **kwargs):
        generator = self.get_objects_generator()
        page = self.paginate_objects_generator(generator)

        if page is None:
            return self.get_paginated_response(None)

        serializer = self.get_serializer(page.object_list, many=True)

        if serializer:
            page.object_list = serializer.data

        return self.get_paginated_response(page)


class RetrieveObjectMixin:
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ListAPIView(ListObjectMixin, GenericObjectAPIView):
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class RetrieveAPIView(RetrieveObjectMixin, GenericObjectAPIView):
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
