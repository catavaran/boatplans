"""Business settings."""
from boatplans.settings.components import config

SITE_NAME = config('SITE_NAME', cast=str, default='Boatplans')

MEASUREMENT_SYSTEM = config('MEASUREMENT_SYSTEM', cast=str, default='imperial')
IS_METRIC_SYSTEM = (MEASUREMENT_SYSTEM == 'metric')


# Use old url-schema for designs
LEGACY_URLS = config('LEGACY_URLS', cast=bool, default=False)
