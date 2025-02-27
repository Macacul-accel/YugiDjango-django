from decouple import config

if config('PIPELINE') == 'production':
    from .prod import *
else:
    from .dev import *