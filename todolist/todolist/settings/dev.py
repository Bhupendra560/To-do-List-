from .base import *        # noqa

DEBUG = True

# Local MySQL Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'todolist_db',
        'USER': 'root',
        'PASSWORD': 'bhupendra560',
        'HOST': 'localhost',
        'PORT': '3306'
    }
}
