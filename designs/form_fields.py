"""Form fields for handling dimensions."""

import re

from django import forms

FEET_RE = re.compile(r"(\d+)('|ft)")
INCHES_RE = re.compile(r'([0-9/]+)("|in)')

MM_PER_FOOT = 304.8
MM_PER_INCH = 25.4


def clean_unit_value(value, unit_factors):
    """
    Convert a string to dimension value (float) using unit factors.

    If string doesn't contain any units then return the same string back.

    >>> unit_factors = (('mm', 1), ('cm', 10))
    >>> clean_unit_value('1mm', unit_factors)
    1.0
    >>> clean_unit_value('1 cm', unit_factors)
    10.0
    >>> clean_unit_value('100', unit_factors)
    '100'
    """
    if isinstance(value, str):
        norm_value = value.replace(' ', '').replace(',', '.').lower()
        for unit, factor in unit_factors:
            unit = unit.replace(' ', '')
            if norm_value.endswith(unit):
                return float(norm_value[: -len(unit)]) * factor
    return value


def extract_feets_inches(value):
    """
    Extract feets and inches from imperial length string.

    >>> extract_feets_inches('1 ft 2 in')
    ('1', '2')
    >>> extract_feets_inches('4"')
    ('0', '4')
    """
    norm_value = value.replace(' ', '').replace(',', '.').lower()
    feets_m = FEET_RE.search(norm_value)
    inches_m = INCHES_RE.search(norm_value)
    feets = feets_m.group(1) if feets_m else '0'
    inches = inches_m.group(1) if inches_m else '0'
    return feets, inches


def clean_imperial_size_value(value):
    """
    Convert imperial size value (feets & inches) to millimeters (int).

    >>> clean_imperial_size_value('1 ft 1/2 in')
    318
    >>> clean_imperial_size_value('1"')
    25
    """
    if isinstance(value, str):
        feets, inches = extract_feets_inches(value)

        feets = int(feets)
        if inches.endswith('1/2'):
            if len(inches) > 3:
                inches = int(inches[:-3]) + 0.5
            else:
                inches = 0.5
        else:
            inches = int(inches)

        if feets + inches > 0:
            return int(round(MM_PER_FOOT * feets + MM_PER_INCH * inches))

    return int(value)


class SizeFormField(forms.IntegerField):
    """Form field for dimension values."""

    def clean(self, size):
        """
        Convert size (metric and imperial) to millimeters.

        >>> field = SizeFormField()
        >>> field.clean('1,23 m')
        1230
        >>> field.clean('1 ft 1/2 in')
        318
        """
        unit_factors = (
            ('mm', 1),
            ('мм', 1),
            ('cm', 10),
            ('см', 10),
            ('m', 1000),
            ('м', 1000),
        )
        size = clean_unit_value(size, unit_factors)
        if isinstance(size, str):
            size = clean_imperial_size_value(size)
        return super().clean(size)


class AreaFormField(forms.DecimalField):
    """Form field for area values."""

    def clean(self, area):
        """
        Convert imperial area to square meters.

        Metric area will be returned as is.

        >>> field = AreaFormField()
        >>> field.clean('10')
        Decimal('10')
        >>> field.clean('10 sq.ft.')
        Decimal('0.929030')
        """
        if isinstance(area, str):
            unit_factors = (
                ('sq.ft', 0.092903),
                ('sq.ft.', 0.092903),
                ('sq ft', 0.092903),
                ('sqf', 0.092903),
                ('sf', 0.092903),
            )
            area = clean_unit_value(area, unit_factors)
            if isinstance(area, float):
                area = '{0:.6f}'.format(area)
        return super().clean(area)


class WeightFormField(forms.IntegerField):
    """Form field for weight values."""

    def clean(self, weight):
        """
        Convert weight (metric and imperial) to grams.

        >>> field = WeightFormField()
        >>> field.clean('1,5kg')
        1500
        >>> field.clean('100 lbs')
        45359
        """
        if isinstance(weight, str):
            unit_factors = (
                ('kg', 1000),
                ('кг', 1000),
                ('t', 1000 * 1000),
                ('т', 1000 * 1000),
                ('lbs.', 453.59237),
                ('lbs', 453.59237),
                ('lb.', 453.59237),
                ('lb', 453.59237),
            )
            weight = clean_unit_value(weight, unit_factors)
            if isinstance(weight, float):
                weight = int(round(weight))
        return super().clean(weight)
