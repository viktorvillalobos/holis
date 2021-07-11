from rest_framework.pagination import CursorPagination


class UserCursoredPagination(CursorPagination):
    ordering = "id"
