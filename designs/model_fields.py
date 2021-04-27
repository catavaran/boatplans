"""Model fields for handling dimensions."""

from django.db import models

from designs import form_fields


class ModelFieldFormClassMixin(object):
    """Override form field class and constructor defaults for model field."""

    init_kwargs = {}
    form_class = None

    def __init__(self, *args, **kwargs):
        """Add default arguments to constructor."""
        super().__init__(*args, **{**self.init_kwargs, **kwargs})

    def formfield(self, **kwargs):
        """User specified form field class."""
        return super().formfield(**{'form_class': self.form_class, **kwargs})


class SizeField(ModelFieldFormClassMixin, models.PositiveIntegerField):
    """Model field for dimension values."""

    init_kwargs = {'null': True, 'blank': True}
    form_class = form_fields.SizeFormField


class AreaField(ModelFieldFormClassMixin, models.DecimalField):
    """Model field for area values."""

    init_kwargs = {'max_digits': 15, 'decimal_places': 6, 'null': True, 'blank': True}
    form_class = form_fields.AreaFormField


class WeightField(ModelFieldFormClassMixin, models.PositiveIntegerField):
    """Model field for weight values."""

    init_kwargs = {'null': True, 'blank': True}
    form_class = form_fields.WeightFormField


class OptionalCharField(models.CharField):
    """CharField with null/blank attributes set to True."""

    def __init__(self, *args, **kwargs):  # noqa: D107
        defaults = {'null': True, 'blank': True, 'max_length': 10}
        super().__init__(*args, **{**defaults, **kwargs})
