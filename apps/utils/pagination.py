from rest_framework.pagination import CursorPagination


def paginate_response(queryset, request, serializer_class, **kwargs):
    pagination_class = kwargs.get("pagination_class") or CursorPagination
    page_size = kwargs.get("page_size") or 10

    paginator = pagination_class()
    paginator.page_size = page_size
    result_page = paginator.paginate_queryset(queryset, request)
    serialized_data = serializer_class(result_page, many=True).data

    return paginator.get_paginated_response(serialized_data)
