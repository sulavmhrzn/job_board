from rest_framework import pagination


class JobsResultSetPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
