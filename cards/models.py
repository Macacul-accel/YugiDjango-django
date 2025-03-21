from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User

class Card(models.Model):
    name = models.CharField(max_length=255, db_index=True, null=False)
    type = models.CharField(max_length=40, db_index=True, null=False)
    frame_type = models.CharField(max_length=40, db_index=True, null=False, default='monster')
    effect = models.TextField(null=False)
    attack = models.IntegerField(db_index=True, null=True)
    defense = models.IntegerField(db_index=True, null=True)
    level_rank = models.IntegerField(validators=[MaxValueValidator(12)], db_index=True, null=True)
    spell_trap_race = models.CharField(max_length=30, db_index=True, null=True)
    monster_race = models.CharField(max_length=30, db_index=True, null=True)
    attribute = models.CharField(max_length=10, db_index=True, null=True)
    archetype = models.CharField(max_length=50, db_index=True, null=True)
    image_url = models.URLField(null=True, db_index=True)

    def __str__(self):
        return self.name

class Deck(models.Model):
    name = models.CharField(max_length=150, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cards = models.ManyToManyField(Card, through='DeckCard',related_name='decks')
    extra_deck = models.ManyToManyField(Card, through='ExtraDeckCard', related_name='extra_decks')
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return self.name
    
class DeckCard(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, db_index=True, related_name='main_cards')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, db_index=True)
    quantity = models.PositiveIntegerField(validators=[MaxValueValidator(3)], default=1)

    # Empêche d'avoir un doublon si la quantité max est atteinte
    class Meta:
        unique_together = ('deck', 'card')

class ExtraDeckCard(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, db_index=True, related_name='extra_cards')
    card = models.ForeignKey(Card, on_delete=models.CASCADE, db_index=True)
    quantity = models.PositiveIntegerField(validators=[MaxValueValidator(3)], default=1)

    class Meta:
        unique_together = ('deck', 'card')