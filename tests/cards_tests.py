import pytest
from rest_framework import status
from cards.models import Deck, DeckCard, ExtraDeckCard


@pytest.mark.django_db
def test_card_creation(card):
    assert card.name == "Blue-Eyes White Dragon"
    assert card.attack == 3000

@pytest.mark.django_db
def test_deck_creation(deck):
    assert deck.name == "Test Deck"

@pytest.mark.django_db
def test_add_card_to_deck(deck, card):
    deck_card = DeckCard.objects.create(deck=deck, card=card, quantity=1)
    
    assert deck_card.deck == deck
    assert deck_card.card == card
    assert deck_card.quantity == 1

@pytest.mark.django_db
def test_add_card_to_extra_deck(deck, card):
    extra_deck_card = ExtraDeckCard.objects.create(deck=deck, card=card, quantity=1)

    assert extra_deck_card.deck == deck
    assert extra_deck_card.card == card

@pytest.mark.django_db
def test_deck_api_list(client, user):
    client.force_authenticate(user=user)
    url = '/api/v2/decks/'

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_create_deck_api(client, user, card):
    client.force_authenticate(user=user)
    url = '/api/v2/decks/'
    data = {
        "name": "New Deck",
        "main_cards": [
            {
                'card': card.id,
                'quantity': 2
            }
        ]    
    }

    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert Deck.objects.filter(name="New Deck").exists()

@pytest.mark.django_db
def test_add_card_to_deck_api(client, user, deck, card):
    client.force_authenticate(user=user)
    url = f'/api/v2/decks/{deck.id}/'
    data = {"name": deck.name, "main_cards": [{"card": card.id, "quantity": 2}]}

    response = client.put(url, data, format='json')

    assert response.status_code in [status.HTTP_200_OK, status.HTTP_201_CREATED]
    assert DeckCard.objects.filter(deck=deck, card=card).exists()
