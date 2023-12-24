import os

# Select the appropriate settings module based on the environment
ENVIRONMENT = os.environ.get('DJANGO_ENV', 'dev')

# Import common settings
from .base import *    # noqa

# Import environment-specific settings
if ENVIRONMENT == 'prod':
    from .prod import *     # noqa
elif ENVIRONMENT == 'ci':
    from .ci import *       # noqa
else:
    from .dev import *      # noqa
