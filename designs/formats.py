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


def humanize_metric_size(size):
    """
    Convert size (millimeters) to human readable string in metric system.

    >>> humanize_metric_size(None)
    >>> humanize_metric_size(1000)
    '1 m'
    >>> humanize_metric_size(1500)
    '1.5 m'
    """
    if not size:
        return None

    meters = '{0:.2f}'.format(size / 1000.0).rstrip('0').rstrip('.')
    return str(_('{meters} m')).format(meters=meters)


def humanize_imperial_size(size):
    """
    Convert size (millimeters) to human readable string in imperial system.

    >>> humanize_imperial_size(None)
    >>> humanize_imperial_size(25)
    '1"'
    >>> humanize_imperial_size(305)
    "1'"
    >>> humanize_imperial_size(330)
    '1\\' 1"'
    """  # noqa: D301, WPS342
    if not size:
        return None

    total_inches = round(size / 25.4)
    feet = int(total_inches / 12)
    inches = int(total_inches % 12)

    if feet > 10:
        # Round inches for long boats
        if inches == 1:
            inches = 0
        elif inches == 11:
            inches = 0
            feet += 1

    size = "{0}'".format(feet) if feet else ''
    if inches:
        return '{0} {1}"'.format(size, inches).strip()
    return size


def humanize_metric_area(area):
    """
    Convert area (sq.meters) to human readable string in metric system.

    >>> humanize_metric_area(None)
    >>> humanize_metric_area(11.5)
    '11.5 m²'
    >>> humanize_metric_area(11.0)
    '11 m²'
    """
    if not area:
        return None
    sqm = '{0:.1f}'.format(area).rstrip('0').rstrip('.')
    return str(_('{area} m²')).format(area=sqm)


def humanize_imperial_area(area):
    """
    Convert area (sq.meters) to human readable string in imperial system.

    >>> humanize_imperial_area(None)
    >>> humanize_imperial_area(11.5)
    '124 sq. ft.'
    """
    if not area:
        return None
    sqf = round(float(area) / 0.0929)
    return str(_('{area} sq. ft.')).format(area=sqf)