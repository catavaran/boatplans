"""Media settings."""

from boatplans.settings.components import config

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

MEDIA_ROOT = config('MEDIA_ROOT')
MEDIA_URL = config('MEDIA_URL', '/media/')

STATIC_ROOT = config('STATIC_ROOT')
STATIC_URL = config('STATIC_URL', '/static/')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_ENABLED = True

THUMBNAIL_PRESERVE_FORMAT = True
THUMBNAIL_QUALITY = 95
