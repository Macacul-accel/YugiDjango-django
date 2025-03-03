from django.urls import path
from .views import CardsList

urlpatterns = [
    path('cards/', CardsList.as_view(), name='cards-list'),
]