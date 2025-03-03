from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import NumberFilter, ChoiceFilter
from django.core.cache import cache

from .constants import *
from .models import Card

def get_cached_distinct_filter_values(field):
    """
    Mis en cache des mots clés pour les filtres, car ChoiceFilter ,choices= effectue des queries non nécessaire
    """
    cache_key = f'distinct_{field}'
    values = cache.get(cache_key)

    if values is None:
        values = list(Card.objects.values_list(field, flat=True).distinct())
        cache.set(cache_key, values, timeout=(60*60)) # 1heure dans le cache

    return values

class CardFilter(FilterSet):
    """
    Les variables *_CHOCIES sont dans le fichier 'constant.py'
    """
    type = ChoiceFilter(choices=MONSTER_TYPE_CHOICES, field_name='monster_type')
    frame_type = ChoiceFilter(choices=FRAME_TYPE_CHOICES, field_name='card_type')
    min_attack = NumberFilter(field_name='attack', lookup_expr='gte')
    max_attack = NumberFilter(field_name='attack', lookup_expr='lte')
    min_defense = NumberFilter(field_name='defense', lookup_expr='gte')
    max_defense = NumberFilter(field_name='defense', lookup_expr='lte')
    min_level_rank = NumberFilter(field_name='level_rank', lookup_expr='gte')
    max_level_rank = NumberFilter(field_name='level_rank', lookup_expr='lte')
    spell_trap_race = ChoiceFilter(choices=[(key, key) for key in get_cached_distinct_filter_values('spell_trap_race')], field_name='spell_trap_race')
    monster_race = ChoiceFilter(choices=[(key, key) for key in get_cached_distinct_filter_values('monster_race')], field_name='monster_race')
    attribute = ChoiceFilter(choices=[(key, key) for key in get_cached_distinct_filter_values('attribute')], field_name='attribute')
    archetype = ChoiceFilter(choices=[(key, key) for key in get_cached_distinct_filter_values('archetype')], field_name='archetype')

    class Meta:
        model = Card
        fields = (
            'type',
            'frame_type',
            'min_attack', 'max_attack',
            'min_defense', 'max_defense',
            'min_level_rank', 'max_level_rank',
            'spell_trap_race',
            'monster_race',
            'attribute',
            'archetype'
        )

    # Filtre personnalisé qui permet d'avoir plusieurs valeur dans un mot clé
    def filter_by_monster_type(self, queryset, name, value):
        return filter_by_mapping(queryset, MONSTER_TYPE_MAPPING, name, value, 'type')

    def filter_by_frametype(self, queryset, name, value):
        return filter_by_mapping(queryset, FRAME_TYPE_MAPPING, name, value, 'frame_type')