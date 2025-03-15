from .models import Card, Deck, DeckCard, ExtraDeckCard

from django.core.validators import MinValueValidator, MaxValueValidator

from rest_framework import serializers

class CardSerializer(serializers.ModelSerializer):
    is_extra = serializers.SerializerMethodField()

    def get_is_extra(self, obj):
        return obj.frame_type in [
            'synchro',
            'synchro_pendulum',
            'fusion',
            'fusion_pendulum',
            'xyz',
            'xyz_pendulum',
            'link',
        ]

    class Meta:
        model = Card
        fields = '__all__'

class DeckCardSerializer(serializers.ModelSerializer):
    card_name = serializers.CharField(source='card.name', read_only=True)
    card_image_url = serializers.URLField(source='card.image_url', read_only=True)
    id = serializers.PrimaryKeyRelatedField(source='card', queryset=Card.objects.all())
    quantity = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)])

    class Meta:
        model = DeckCard
        fields = (
            'card_name', 'card_image_url', 'id', 'quantity',
        )

class ExtraDeckCardSerializer(serializers.ModelSerializer):
    card_name = serializers.CharField(source='card.name', read_only=True)
    card_image_url = serializers.URLField(source='card.image_url', read_only=True)
    id = serializers.PrimaryKeyRelatedField(source='card', queryset=Card.objects.all())
    quantity = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)])

    class Meta:
        model = ExtraDeckCard
        fields = (
            'card_name', 'card_image_url', 'id', 'quantity',
        )

class DeckSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    main_cards = DeckCardSerializer(many=True, required=False)
    extra_cards = ExtraDeckCardSerializer(many=True, required=False)
    main_deck_total = serializers.SerializerMethodField()
    extra_deck_total = serializers.SerializerMethodField()

    def get_main_deck_total(self, obj):
        deck_cards = obj.main_cards.all()
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

    def validate(self, data):
        main_deck_data = data.get('main_cards', [])
        extra_deck_data = data.get('extra_cards', [])

        main_deck_total = sum(main_card_data.get('quantity', 0) for main_card_data in main_deck_data)
        extra_deck_total = sum(extra_card_data.get('quantity', 0) for extra_card_data in extra_deck_data)

        if main_deck_total > 60:
            raise serializers.ValidationError("Un deck ne peut pas contenir plus de 60 cartes.")
        if extra_deck_total > 15:
            raise serializers.ValidationError("L'extra deck ne peut pas contenir plus de 15 cartes.")
        
        return data

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
        # Update the deck name
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        main_cards_data = validated_data.pop('main_cards', [])
        extra_cards_data = validated_data.pop('extra_cards', [])

        # Récupération des données des cartes pour mettre à jour la quantité ou encore retirer/ajouter au deck
        existing_main_cards = {card.card_id: card for card in instance.main_cards.all()}
        new_main_cards = {card_data['card'].id: card_data for card_data in main_cards_data}

        # Suppression des cartes qui ne sont plus dans la liste
        for removed_card in existing_main_cards:
            if removed_card not in new_main_cards:
                existing_main_cards[removed_card].delete()
        
        # Mis à jour de la quantité, ou création de l'instance pour les nouvelles cartes
        for card_id, card_data in new_main_cards.items():
            DeckCard.objects.update_or_create(deck=instance, card_id=card_id, defaults=card_data)

        existing_extra_cards = {card.card_id: card for card in instance.extra_cards.all()}
        new_extra_cards = {card_data['card'].id: card_data for card_data in extra_cards_data}
        
        for removed_card in existing_extra_cards:
            if removed_card not in new_extra_cards:
                existing_extra_cards[removed_card].delete()

        for card_id, card_data in new_extra_cards.items():
            ExtraDeckCard.objects.update_or_create(deck=instance, card_id=card_id, defaults=card_data)

        return instance