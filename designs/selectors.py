"""Selectors and getters for design app."""

from django.conf import settings

from designs.models import Design


def get_length_intervals():
    """Return list of length intervals depending on measurement system."""
    if settings.IS_METRIC_SYSTEM:
        return ((0, 4), (4, 6), (6, 8), (8, 10), (10, 99))
    return ((0, 10), (10, 14), (14, 18), (18, 24), (24, 30), (30, 36), (36, 99))


def get_lengths_for_propulsion(propulsion):
    """Return list of available length intervals for designs of specified propulsion."""
    return [
        (from_length, to_length)
        for from_length, to_length in get_length_intervals()
        if get_designs_by_length(from_length, to_length, propulsion=propulsion)
    ]


def get_designs_by_length(from_length, to_length, **filters):
    qs = Design.objects.filter(designer__enabled=True, enabled=True, **filters)
    # metres or feets
    multiplier = 1000 if settings.IS_METRIC_SYSTEM else 305
    if from_length:
        qs = qs.filter(loa__gte=multiplier * int(from_length))
    if to_length:
        qs = qs.filter(loa__lte=multiplier * int(to_length))
    return qs