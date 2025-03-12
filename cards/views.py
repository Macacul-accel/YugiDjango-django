from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, viewsets
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from .filters import CardFilter
from .models import Card, Deck
from .serializers import CardSerializer, DeckSerializer

class CustomPagination(PageNumberPagination):
    page_size = 20
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100

"""
Retourne la liste de toutes les cartes, et mis en place des différents filtres
"""
class CardsList(ListAPIView):
    queryset = Card.objects.defer('effect', 'image_url').all().order_by('id')
    serializer_class = CardSerializer
    filterset_class = CardFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        ]
    search_fields = ['name']
    pagination_class = CustomPagination
    permission_classes = [AllowAny]

    #cache for 10 minutes
    @method_decorator(cache_page(60 * 10))
    def dispatch(self, *args, **kwargs):
        return super(CardsList, self).dispatch(*args, **kwargs)

"""
Espace de deck building pour chaque utilisateur
Séparation du main deck et de l'extra deck
"""
class DeckViewSet(viewsets.ModelViewSet):
    queryset = Deck.objects.prefetch_related('main_cards__card', 'extra_cards__card')
    serializer_class = DeckSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 20
    pagination_class.page_query_param = 'page'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)
    
