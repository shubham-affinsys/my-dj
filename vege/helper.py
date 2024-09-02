from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import pagination
from django.core.paginator import Paginator

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 2

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 2

class paginate(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
                    "count": 39,
                    "next":  self.get_next_link(),
                    "previous": self.get_previous_link(),
                    "results": data
                })
