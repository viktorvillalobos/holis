from rest_framework.pagination import CursorPagination


class MessageCursoredPagination(CursorPagination):
    page_size = 10
