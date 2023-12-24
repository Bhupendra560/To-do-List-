import os

# Select the appropriate settings module based on the environment
ENVIRONMENT = os.environ.get('DJANGO_ENV', 'dev')

# Import common settings
from .base import *

# Import environment-specific settings
if ENVIRONMENT == 'prod':
    from .prod import *
elif ENVIRONMENT == 'ci':
    from .ci import *
else:
    from .dev import *