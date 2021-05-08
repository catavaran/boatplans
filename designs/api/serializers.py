"""Serializers for design app."""

from django.conf import settings
from rest_framework import serializers

from designs.formats import humanize_imperial_size, humanize_metric_size, humanize_size_range
from designs.models import Design, Designer, Propulsion
from designs.selectors import get_lengths_for_propulsion


class SerializerSizeField(serializers.Field):
    def to_representation(self, size):
        return {
            'metric': humanize_metric_size(size),
            'imperial': humanize_imperial_size(size),
        }


class DesignerLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designer
        fields = ['slug', 'name']


class PropulsionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Propulsion
        fields = ['slug', 'long_name']


class PropulsionWithLengthsSerializer(serializers.ModelSerializer):
    lengths = serializers.SerializerMethodField()

    class Meta:
        model = Propulsion
        fields = ['slug', 'long_name', 'lengths']

    def get_lengths(self, propulsion):
        slug_format = '{0}-{1}' if settings.IS_METRIC_SYSTEM else '{0}ft-{1}ft'
        unit = 'м' if settings.IS_METRIC_SYSTEM else 'ft'
        return [
            {
                'slug': slug_format.format(size_from, size_to),
                'label': humanize_size_range(size_from, size_to, unit),
            }
            for (size_from, size_to) in get_lengths_for_propulsion(propulsion)
        ]

class DesignCardSerializer(serializers.ModelSerializer):
    designer = DesignerLightSerializer()
    loa = SerializerSizeField()
    class Meta:
        model = Design
        fields = ['slug', 'name', 'designer', 'tiny_description', 'loa', 'image']
