"""Serializers for design app."""

from django.conf import settings
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from designs.formats import (
    humanize_imperial_area,
    humanize_imperial_size,
    humanize_metric_area,
    humanize_metric_size,
    humanize_size_range,
)
from designs.models import Design, Designer, Propulsion
from designs.selectors import get_lengths_for_propulsion


class SerializerThumbnailImageField(serializers.Field):
    def __init__(self, *args, **kwargs):
        self.size = kwargs.pop('size')
        super().__init__(*args, *kwargs)

    def to_representation(self, image):
        double_size = (self.size[0] * 2, self.size[1] * 2)
        default_image = self.get_thumbnail(image, self.size)
        double_image = self.get_thumbnail(image, double_size)
        webp_image = self.get_thumbnail(image, self.size, format='WEBP')
        webp_double_image = self.get_thumbnail(image, double_size, format='WEBP')

        return {
            'original': image.url,
            'src': default_image.url,
            'srcset': self.build_srcset(default_image, double_image),
            'width': default_image.width,
            'height': default_image.height,
            'sources': [
                {
                    'srcset': self.build_srcset(webp_image, webp_double_image),
                    'type': 'image/webp',
                }
            ],
        }

    def get_thumbnail(self, image, size, format=None):
        kwargs = {'format': format} if format else {}
        return get_thumbnail(image, '{0}x{1}'.format(*size), **kwargs)

    def build_srcset(self, image, image_2x):
        return '{0}, {1} 2x'.format(image.url, image_2x.url)


class SerializerSizeField(serializers.Field):
    def to_representation(self, size):
        return {
            'metric': humanize_metric_size(size),
            'imperial': humanize_imperial_size(size),
        }


class SerializerAreaField(serializers.Field):
    def to_representation(self, area):
        return {
            'metric': humanize_metric_area(area),
            'imperial': humanize_imperial_area(area),
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
    absolute_url = serializers.CharField(source='get_absolute_url')
    image = SerializerThumbnailImageField(size=(120, 120))
    designer = DesignerLightSerializer()
    loa = SerializerSizeField()

    class Meta:
        model = Design
        fields = [
            'slug',
            'absolute_url',
            'image',
            'name',
            'designer',
            'tiny_description',
            'loa',
        ]


class DesignListSerializer(serializers.ModelSerializer):
    absolute_url = serializers.CharField(source='get_absolute_url')
    image = SerializerThumbnailImageField(size=(64, 64))
    designer = DesignerLightSerializer()
    loa = SerializerSizeField()
    beam = SerializerSizeField()
    sail_area = SerializerAreaField()
    horse_power = serializers.CharField(source='horsepower')

    class Meta:
        model = Design
        fields = [
            'slug',
            'absolute_url',
            'image',
            'name',
            'designer',
            'tiny_description',
            'loa',
            'beam',
            'sail_area',
            'horse_power',
        ]
