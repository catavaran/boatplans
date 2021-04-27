"""
This file contains all the settings used in production.

This file is required and if development.py is present these
values are overridden.
"""

from boatplans.settings.components import config

ALLOWED_HOSTS = (config('DOMAIN_NAME'),)

STATIC_ROOT = config('STATIC_ROOT')
MEDIA_ROOT = config('MEDIA_ROOT')
