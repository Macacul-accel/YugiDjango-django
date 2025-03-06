import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from cards.models import Card, Deck

test_card_data = {
    "name": "Blue-Eyes White Dragon",
    "type": "Monster",
    "frame_type": "monster",
    "effect": "Legendary Dragon",
    "attack": 3000,
    "defense": 2500,
    "level_rank": 8,
    "monster_race": "Dragon",
    "attribute": "Light",
    "archetype": "Blue-Eyes"
}

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpass')

@pytest.fixture
def card(db):
    return Card.objects.create(**test_card_data)

@pytest.fixture
def deck(db, user):
    return Deck.objects.create(name="Test Deck", user=user)

@pytest.fixture
def client():
    return APIClient()