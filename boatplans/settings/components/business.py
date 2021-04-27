"""Business settings."""
from boatplans.settings.components import config

# Use old url-schema for designs
LEGACY_URLS = config('LEGACY_URLS', cast=bool, default=False)
