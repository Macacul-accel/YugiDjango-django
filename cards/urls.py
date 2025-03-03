from django.urls import path, include
from .views import CardsList, DeckViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('decks', DeckViewSet)

urlpatterns = [
    path('cards/', CardsList.as_view(), name='cards-list'),
    path('', include(router.urls)),
]