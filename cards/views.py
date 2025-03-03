from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from .filters import CardFilter
from .models import Card
from .serializers import CardSerializer

class CardsList(ListAPIView):
    queryset = Card.objects.defer('effect', 'image').all().order_by('id')
    serializer_class = CardSerializer
    filterset_class = CardFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        ]
    search_fields = ['name']
    pagination_class = PageNumberPagination
    pagination_class.page_size = 20
    pagination_class.page_query_param = 'page_num'
    pagination_class.page_size_query_param = 'page_size'
    pagination_class.max_page_size = 100
    permission_classes = [AllowAny]
