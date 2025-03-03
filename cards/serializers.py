from .models import Card, Deck, DeckCard, ExtraDeckCard

from rest_framework import serializers

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'

class DeckCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeckCard
        fields = (
            'card', 'quantity',
        )

class ExtraDeckCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraDeckCard
        fields = (
            'card', 'quantity',
        )

class DeckSerializer(serializers.ModelSerializer):
    main_cards = DeckCardSerializer(many=True)
    extra_cards = ExtraDeckCardSerializer(many=True)
    main_deck_total = serializers.SerializerMethodField()
    extra_deck_total = serializers.SerializerMethodField()

    def get_main_deck_total(self, obj):
        deck_cards = obj.cards.all()
        return sum(deck_card.quantity for deck_card in deck_cards)
    
    def get_extra_deck_total(self, obj):
        extra_deck_cards = obj.extra_cards.all()
        return sum(extra_deck_card.quantity for extra_deck_card in extra_deck_cards)

    class Meta:
        model = Deck
        fields = (
            'id', 'name', 'user', 'main_cards', 'extra_cards',
            'main_deck_total', 'extra_deck_total',
        )

    def validate(self, obj):
        if self.get_main_deck_total(obj) > 60:
            raise serializers.ValidationError("Un deck ne peut pas contenir plus de 60 cartes.")
        if self.get_extra_deck_total(obj) > 15:
            raise serializers.ValidationError("L'extra deck ne peut pas contenir plus de 15 cartes.")

    def create(self, validated_data):
        main_cards_data = validated_data.pop('main_cards', [])
        extra_cards_data = validated_data.pop('extra_cards', [])

        deck = Deck.objects.create(**validated_data)

        for main_card_data in main_cards_data:
            DeckCard.objects.create(deck=deck, **main_card_data)
        
        for extra_card_data in extra_cards_data:
            ExtraDeckCard.objects.create(deck=deck, **extra_card_data)

        return deck
    
    def update(self, instance, validated_data):
        main_cards_data = validated_data.pop('main_cards', [])
        extra_cards_data = validated_data.pop('extra_cards', [])

        instance.cars.clear()
        instance.extra_cards.clear()

        for main_card_data in main_cards_data:
            DeckCard.objects.update_or_create(deck=instance, **main_card_data)

        for extra_card_data in extra_cards_data:
            ExtraDeckCard.objects.update_or_create(deck=instance, **extra_card_data)

        return instance