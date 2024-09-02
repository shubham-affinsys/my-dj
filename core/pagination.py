from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from core import cache
import logging
logger = logging.getLogger('mydj')

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 2

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 2

class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        response = {
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        }
        return Response(response)

