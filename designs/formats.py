"""Formatting utils."""

from django.utils.translation import ugettext_lazy as _


def humanize_size_range(size_from, size_to, unit='ft'):
    """
    Convert size range to human readable string.

    >>> humanize_size_range(0, 10)
    'up to 10 ft'
    >>> humanize_size_range(10, 14)
    '10-14 ft'
    >>> humanize_size_range(16, 99)
    'from 16 ft'
    >>> humanize_size_range(10, 14, 'm')
    '10-14 m'
    """
    size_from = int(size_from) if size_from else 0
    size_to = int(size_to) if size_to else 0

    if size_to == 99:
        return str(_('from {size_from} {unit}')).format(size_from=size_from, unit=unit)

    if size_from == 0:
        return str(_('up to {size_to} {unit}')).format(size_to=size_to, unit=unit)

    return str(_('{size_from}-{size_to} {unit}')).format(
        size_from=size_from, size_to=size_to, unit=unit
    )
