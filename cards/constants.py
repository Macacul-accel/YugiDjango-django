def filter_by_mapping(queryset, mapping, name, value, field):
    filter_values = mapping.get(value)
    if filter_values:
        filter_kwargs = {f"{field}__in": filter_values}
        return queryset.filter(**filter_kwargs)
    return queryset

# Génère les mots clés pour le filtre
def generate_choices(mapping):
    return [(key, key.capitalize()) for key in mapping.keys()]

FRAME_TYPE_MAPPING = {
    'spell': ['spell'],
    'trap': ['trap'],
    'monster': [
        'normal',
        'effect',
        'ritual_pendulum',
        'effect_pendulum',
        'normal_pendulum',
        'ritual',
    ],
    'extra-deck': [
        'synchro',
        'synchro_pendulum',
        'fusion',
        'fusion_pendulum',
        'xyz',
        'xyz_pendulum',
        'link',
    ]
}

MONSTER_TYPE_MAPPING = {
    'normal': ['Normal Monster', 'Normal Tuner Monster', 'Pendulum Normal Monster'],
    'effect': ['Effect Monster'],
    'ritual': ['Ritual Effect Monster', 'Ritual Monster', 'Pendulum Effect Ritual Monster',],
    'fusion': ['Fusion Monster', 'Pendulum Effect Fusion Monster'],
    'synchro': [
        'Synchro Monster',
        'Synchro Pendulum Effect Monster',
        'Synchro Tuner Monster',
    ],
    'xyz': ['XYZ Monster', 'XYZ Pendulum Effect Monster'],
    'toon': ['Toon Monster'],
    'spirit': ['Spirit Monster'],
    'union': ['Union Effect Monster'],
    'gemini': ['Gemini Monster'],
    'tuner': [
        'Normal Tuner Monster',
        'Flip Tuner Effect Monster',
        'Tuner Monster',
        'Synchro Tuner Monster',
        'Pendulum Tuner Effect Monster',
    ],
    'flip': ['Pendulum Flip Effect Monster', 'Flip Effect Monster', 'Flip Tuner Effect Monster'],
    'pendulum': [
        'Pendulum Normal Monster',
        'Pendulum Effect Monster',
        'Pendulum Flip Effect Monster',
        'Pendulum Effect Ritual Monster',
        'Pendulum Effect Fusion Monster',
        'Pendulum Tuner Effect Monster',
        'Synchro Pendulum Effect Monster',
        'XYZ Pendulum Effect Monster',
    ],
    'link': ['Link Monster'],
}

FRAME_TYPE_CHOICES = generate_choices(FRAME_TYPE_MAPPING)
MONSTER_TYPE_CHOICES = generate_choices(MONSTER_TYPE_MAPPING)