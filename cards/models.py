from django.db import models
from django.core.validators import MaxValueValidator

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
    image = models.ImageField(upload_to='card_images/', null=False, default='card_images/default.jpg')

    def __str__(self):
        return self.name
