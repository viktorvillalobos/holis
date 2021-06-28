from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from django.db import models
from django.db.models import Q, Subquery
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param
from rest_framework.views import APIView

import json
from __future__ import annotations
from collections import OrderedDict
from collections.abc import Sequence
from copy import deepcopy


class CursoredPage(Sequence):
    def __init__(self, *, object_list: List, next_page_cursor, previous_page_cursor):
        self.object_list = object_list
        self.next_page_cursor = next_page_cursor
        self.previous_page_cursor = previous_page_cursor

    def __repr__(self) -> str:
        if not self.object_list:
            return "<CursoredPage empty>"
        return f"<CursoredPage from {self.object_list[0]} to {self.object_list[-1]}>"

    def __len__(self) -> int:
        return len(self.object_list)

    def __getitem__(self, item) -> Any:
        if not isinstance(item, (int, slice)):
            raise TypeError(
                f"CursoredPage indices must be integers or slices, not {type(item).__name__}."
            )

        return self.object_list[item]

    def _reversed(self) -> CursoredPage:
        self.next_page_cursor, self.previous_page_cursor = (
            self.previous_page_cursor,
            self.next_page_cursor,
        )
        self.object_list = list(self.object_list[::-1])
        return self


class CursoredServicePaginator:
    def __init__(self, cursored_service: Union[Callable], page_size: int):
        self.cursored_service = cursored_service
        self.page_size = page_size

    def get_next(
        self, reverse: bool = False, page_size: Optional[int] = None, **kwargs
    ):
        page_size = page_size or self.page_size
        items, next_page_cursor, previous_page_cursor = self.cursored_service(
            reverse=reverse, page_size=page_size, **kwargs
        )
        return CursoredPage(
            object_list=items,
            next_page_cursor=next_page_cursor,
            previous_page_cursor=previous_page_cursor,
        )

    def get_previous(
        self, reverse: bool = False, page_size: Optional[int] = None, **kwargs
    ):
        return self.get_next(
            reverse=not reverse, page_size=page_size, **kwargs
        )._reversed()


class CursoredAPIPagination:
    display_page_controls = False
    max_page_size: int = 100
    page_size: int = 100
    paginator_class = CursoredServicePaginator

    def __init__(
        self,
        page_size: Optional[int] = None,
        max_page_size: Optional[int] = None,
        paginator_class=None,
        request: Optional[Request] = None,
        view: Optional[APIView] = None,
    ):
        self.paginator_class = paginator_class or self.paginator_class
        self.request = request
        self.view = view
        self.page_size = page_size or self.page_size
        self.max_page_size = max_page_size or self.max_page_size
        self.page_size = min(max(2, self.page_size), self.max_page_size)

    def get_cursor_from_request(self, request: Request) -> Optional[Dict]:
        params = request.query_params
        cursor = params.get("cursor")

        if cursor:
            bytes_data = urlsafe_base64_decode(cursor)
            str_data = force_str(bytes_data)
            decoded_data = json.loads(str_data)
            return decoded_data

    def paginate(
        self,
        paginable: Callable,
        request: Optional[Request] = None,
        extra_context: Optional[dict] = None,
    ):
        request = request or self.request
        next_page = "next" in request.query_params
        previous_page = "previous" in request.query_params
        cursor = self.get_cursor_from_request(request)
        context = deepcopy(extra_context) or {}
        context["cursor"] = cursor

        paginator = self.paginator_class(paginable, page_size=self.page_size)

        if previous_page and next_page:
            raise ValidationError("Cannot search next and previous page simultaneously")

        if previous_page:
            page = paginator.get_previous(**context)
        else:
            page = paginator.get_next(**context)

        return page

    def get_link(self, base_url, cursor, to: str):
        url = base_url
        url = replace_query_param(url, to, "")

        str_data = json.dumps(cursor)
        bytes_data = force_bytes(str_data)
        encoded_data = urlsafe_base64_encode(bytes_data)

        url = replace_query_param(url, "cursor", encoded_data)

        return url

    def get_paginated_response(
        self,
        page: Optional[type(CursoredPage)] = None,
        request: Optional[type(Request)] = None,
    ):
        request = request or self.request

        if page is None or not page.object_list:
            return Response(
                OrderedDict([("next", None), ("previous", None), ("results", [])])
            )

        data = page.object_list
        next_link = None
        previous_link = None
        base_url = request.build_absolute_uri()
        base_url = remove_query_param(base_url, "next")
        base_url = remove_query_param(base_url, "previous")

        if bool(page.next_page_cursor):
            next_link = self.get_link(
                base_url=base_url, cursor=page.next_page_cursor, to="next"
            )

        if bool(page.previous_page_cursor):
            previous_link = self.get_link(
                base_url=base_url, cursor=page.previous_page_cursor, to="previous"
            )

        return Response(
            OrderedDict(
                [("next", next_link), ("previous", previous_link), ("results", data)]
            )
        )


def get_paginated_queryset(
    queryset: models.QuerySet,
    cursor: Optional[Dict] = None,
    page_size: Optional[int] = 100,
    reverse: Optional[bool] = False,
    order_column: Optional[str] = "created",
    pk_column: Optional[str] = "uuid",
) -> Tuple[List, Optional[Dict[str, str]], Optional[Dict[str, str]]]:
    untie_column = pk_column
    next_page_cursor = None
    previous_page_cursor = None

    if reverse:
        order_by = [f"-{order_column}", f"-{untie_column}"]
        order_column_criteria = untie_column_criteria = "__lt"
    else:
        order_by = [f"{order_column}", f"{untie_column}"]
        order_column_criteria = untie_column_criteria = "__gt"

    if cursor:
        cursor_pk_value = cursor[pk_column]

        subquery = Subquery(
            queryset.filter(**{pk_column: cursor_pk_value})
            .values(f"{order_column}")
            .order_by()[:1]
        )

        q_expr = Q(**{f"{order_column}{order_column_criteria}": subquery}) | Q(
            **{
                f"{order_column}": subquery,
                f"{untie_column}{untie_column_criteria}": cursor_pk_value,
            }
        )
        queryset = queryset.filter(q_expr)

    objects = list(queryset.order_by(*order_by)[: page_size + 1])

    if objects:
        if len(objects) > page_size:
            objects = objects[:page_size]
            last_object = objects[-1]
            next_page_cursor = {pk_column: str(getattr(last_object, pk_column))}

        if cursor:
            first_object = objects[0]
            previous_page_cursor = {pk_column: str(getattr(first_object, pk_column))}

    return objects, next_page_cursor, previous_page_cursor
