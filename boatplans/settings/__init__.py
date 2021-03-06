"""
This is a django-split-settings main file.

For more information read this:
https://github.com/sobolevn/django-split-settings

To change settings file:
`DJANGO_ENV=production python manage.py runserver`
"""

from os import environ

from split_settings.tools import include, optional

# Managing environment via DJANGO_ENV variable:
environ.setdefault('DJANGO_ENV', 'development')
ENV = environ['DJANGO_ENV']

base_settings = [
    'components/common.py',
    'components/db.py',
    'components/auth.py',
    'components/i18n.py',
    'components/media.py',
    'components/business.py',
    # Select the right env:
    'environments/{0}.py'.format(ENV),
    # Optionally override some settings:
    optional('environments/local.py'),
]

# Include settings:
include(*base_settings)
