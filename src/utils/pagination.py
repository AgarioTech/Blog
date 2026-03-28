from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class LargeResultsSetPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'pages': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'results': data
        })

    page_size = 5



class SmallResultsSetPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'pages': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'results': data
        })

    page_size = 1






