"""
This file contains all the settings that defines the development server.

SECURITY WARNING: don't run with debug turned on in production!
"""

from boatplans.settings.components import config
from boatplans.settings.components.common import INSTALLED_APPS, MIDDLEWARE

# Setting the development status:

DEBUG = True

ALLOWED_HOSTS = (
    config('DOMAIN_NAME'),
    'localhost',
    '0.0.0.0',  # noqa: S104
    '127.0.0.1',
    '[::1]',
)

INSTALLED_APPS += ('debug_toolbar',)

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # https://github.com/bradmontgomery/django-querycount
    # Prints how many queries were executed, useful for the APIs.
    'querycount.middleware.QueryCountMiddleware',
)


def custom_show_toolbar(request):
    """Show debug toolbar to superuser only."""
    return request.user.is_superuser


DEBUG_TOOLBAR_CONFIG = {  # noqa: WPS407
    'SHOW_TOOLBAR_CALLBACK': 'boatplans.settings.environments.development.custom_show_toolbar',
}

QUERYCOUNT = {  # noqa: WPS407
    'THRESHOLDS': {
        'MEDIUM': 50,
        'HIGH': 200,
        'MIN_TIME_TO_LOG': 0,
        'MIN_QUERY_COUNT_TO_LOG': 0,
    },
    'IGNORE_REQUEST_PATTERNS': [],
    'IGNORE_SQL_PATTERNS': [],
    'DISPLAY_DUPLICATES': None,
    'RESPONSE_HEADER': 'X-DjangoQueryCount-Count',
}
