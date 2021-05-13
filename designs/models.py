"""Models for designs application."""

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import ImageField

from designs.model_fields import AreaField, OptionalCharField, SizeField, WeightField

# Marker for "show more" button in design description
CUT_MARKER = '--cut--'

HULL_TYPES = (
    ('mono', _('monohull')),
    ('catamaran', _('catamaran')),
    ('trimaran', _('trimaran')),
)

ENGINE_TYPES = (
    ('o', _('outboard')),
    ('i', _('inboard')),
)

LINK_TYPES = (
    ('plan', _('Plans')),
    ('forum', _('Forum')),
    ('site', _('Site')),
    ('blog', _('Building logs')),
    ('saling', _('Sailing reports')),
)

IMAGE_TYPES = (
    ('drawing', _('Drawing')),
    ('photo', _('Photo')),
)

VIDEO_TYPES = (
    ('youtube', 'Youtube'),
    ('vimeo', 'Vimeo'),
)


def path_upload_to(instance, filename):
    """Get upload path for design's image."""
    design = getattr(instance, 'design', instance)
    root_dir = 'plans' if settings.LEGACY_URLS else 'design'
    return '{0}/{1}/{2}/{3}'.format(root_dir, design.designer.slug, design.slug, filename)


class Propulsion(models.Model):
    """Boat propulson (oars, motor, sail)."""

    slug = models.SlugField(_('slug'), unique=True)
    name = models.CharField(_('name'), max_length=10)
    long_name = models.CharField(_('long name'), max_length=50)

    order = models.PositiveIntegerField()

    class Meta(object):
        verbose_name = _('propulsion')
        verbose_name_plural = _('propulsions')
        ordering = ('order', 'id')

    def __str__(self):
        return self.name


class HullConstruction(models.Model):
    """Hull construction (fiberglass, plywood, steel)."""

    slug = models.SlugField(_('slug'), unique=True)
    name = models.CharField(_('name'), max_length=50)

    order = models.PositiveIntegerField()

    class Meta(object):
        verbose_name = _('hull construction')
        verbose_name_plural = _('hull constructions')
        ordering = ('order', 'id')

    def __str__(self):
        return self.name


class BoatKind(models.Model):
    """Boat kind (sport boat, beach catamaran)."""

    slug = models.SlugField(_('slug'), unique=True)
    name = models.CharField(_('name'), max_length=30)

    order = models.PositiveIntegerField()

    class Meta(object):
        verbose_name = _('boat kind')
        verbose_name_plural = _('boat kinds')
        ordering = ('order', 'id')

    def __str__(self):
        return self.name


class Designer(models.Model):
    """Designer (John Welsford, Bruce Robertd, Dufley Dix)."""

    slug = models.SlugField(_('slug'), unique=True)
    name = models.CharField(_('name'), max_length=50)
    url = models.URLField(_('url'), blank=True)
    description = models.TextField(_('description'), blank=True)

    enabled = models.BooleanField(_('enabled'), default=True)

    class Meta(object):
        verbose_name = _('designer')
        verbose_name_plural = _('designers')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Designer's url."""
        return '/{0}/'.format(self.slug)

class Tag(models.Model):
    """Tag for design."""

    slug = models.SlugField(_('slug'), unique=True)
    name = models.CharField(_('name'), max_length=50)

    class Meta(object):
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.name


class Design(models.Model):
    """Boat design."""

    slug = models.SlugField(_('slug'), unique=True)
    name = models.CharField(_('name'), max_length=50)
    tiny_description = models.CharField(
        _('tiny description'),
        max_length=100,
        help_text=_('For example: "fast cruiser" or "power cartop-catamaran"'),
    )
    designer = models.ForeignKey(
        Designer,
        related_name='designs',
        verbose_name=_('designer'),
        on_delete=models.PROTECT,
    )
    url = models.URLField(_('URL'), max_length=250, blank=True)

    tags = models.ManyToManyField(Tag, verbose_name=_('tags'), blank=True)

    meta_description = models.TextField(
        _('meta description'),
        blank=True,
        null=True,
        help_text=_(
            'Default is: "[boat] by [designer]: specs, plans, photo and video gallery"',
        ),
    )
    meta_keywords = OptionalCharField(
        _('meta keywords'),
        max_length=250,
        help_text=_('name, designer, tags and "boat plans" will be added automatically'),
    )

    propulsion = models.ForeignKey(
        Propulsion,
        verbose_name=_('propulsion'),
        on_delete=models.PROTECT,
    )
    hull_type = models.CharField(
        _('hull type'),
        max_length=10,
        default='mono',
        choices=HULL_TYPES,
    )
    hull_constructions = models.ManyToManyField(
        HullConstruction,
        verbose_name=_('hull construction(s)'),
        blank=True,
    )
    kinds = models.ManyToManyField(BoatKind, verbose_name=_('boat kind(s)'), blank=True)

    loa = SizeField(_('length overall'), db_index=True, help_text=_('millimeters'))
    lod = SizeField(_('length on deck'))
    lwl = SizeField(_('waterline length'))
    beam = SizeField(_('beam'))
    bwl = SizeField(_('beam at waterline'))

    draft = SizeField(_('draft'))
    draft_cb_up = SizeField(_('draft (cb up)'))

    depth = SizeField(_('depth'))
    freeboard = SizeField(_('freeboard'))

    weight = WeightField(_('weight'), help_text=_('grams'))
    ballast_weight = WeightField(_('ballast weight'))
    cb_weight = WeightField(_('centerboard weight'))
    displacement = WeightField(_('displacement'))
    capacity = WeightField(_('capacity'))

    sail_area = AreaField(_('sail area'), help_text=_('m2'))
    sail_area_main = AreaField(_('main area'))
    sail_area_jib = AreaField(_('jib area'))
    sail_area_genoa = AreaField(_('genoa area'))
    sail_area_spi = AreaField(_('spi area'))

    accommodation = OptionalCharField(_('accomodation'))
    berths = OptionalCharField(_('berths'))
    headroom = SizeField(_('headroom'))

    horsepower = OptionalCharField(_('engine power'), max_length=20, help_text=_('hp'))
    engine_type = OptionalCharField(_('engine type'), max_length=1, choices=ENGINE_TYPES)

    description = models.TextField(_('description'))

    image = ImageField(_('main image'), upload_to=path_upload_to, max_length=250)

    price = OptionalCharField(_('price'), max_length=20)
    kit_price = OptionalCharField(_('kit price'), max_length=20)

    lang = models.CharField(
        _('main language'),
        max_length=2,
        default=settings.LANGUAGE_CODE.split('-')[0],
    )

    see_also = models.ManyToManyField('self', verbose_name=_('see also'), blank=True)

    enabled = models.BooleanField(_('enabled'), default=True)

    score = models.IntegerField(_('score'), default=0)
    last_update = models.DateTimeField(null=True, auto_now=True)

    class Meta(object):
        verbose_name = _('design')
        verbose_name_plural = _('designs')
        ordering = ('loa', 'id')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Design's url."""
        # XXX `django.urls.reverse` can't be used here
        if settings.LEGACY_URLS:
            return '/{0}/'.format(self.slug)

        return '/{0}/{1}/'.format(self.designer.slug, self.slug)


class Image(models.Model):
    """Boat drawing or photo."""

    design = models.ForeignKey(
        Design,
        verbose_name=_('design'),
        related_name='images',
        on_delete=models.PROTECT,
    )
    image_type = models.CharField(_('image type'), max_length=7, choices=IMAGE_TYPES)
    image = ImageField(_('image'), upload_to=path_upload_to, max_length=250)
    title = OptionalCharField(_('title'), max_length=100)
    image_url = models.URLField(_('original image URL'), max_length=250, null=True, blank=True)

    order = models.PositiveIntegerField()

    def __str__(self):
        return self.title

    class Meta(object):
        verbose_name = _('design image')
        verbose_name_plural = _('design images')
        ordering = ('order', 'id')


class Video(models.Model):
    """Video about design."""

    design = models.ForeignKey(
        Design,
        verbose_name=_('design'),
        related_name='videos',
        on_delete=models.PROTECT,
    )
    video_type = models.CharField(_('video type'), max_length=10, choices=VIDEO_TYPES)
    video_id = models.CharField(_('video id'), max_length=200)
    image = ImageField(_('preview'), upload_to=path_upload_to, max_length=250)
    title = OptionalCharField(_('title'), max_length=200)
    description = models.TextField(_('description'), null=True, blank=True)

    order = models.PositiveIntegerField()

    def __str__(self):
        return self.title

    class Meta(object):
        verbose_name = _('design video')
        verbose_name_plural = _('design video')
        ordering = ('order', 'id')

    def get_video_url(self):
        """Get URL of the video."""
        if self.video_type == 'youtube':
            return 'http://www.youtube.com/watch?v={0}'.format(self.video_id)
        if self.video_type == 'vimeo':
            return 'http://vimeo.com/{0}'.format(self.video_id)
        return ''


class Link(models.Model):
    """Link to design-related page."""

    design = models.ForeignKey(
        Design,
        verbose_name=_('design'),
        related_name='links',
        on_delete=models.PROTECT,
    )
    image = ImageField(_('image'), upload_to=path_upload_to, max_length=250)
    link_type = models.CharField(_('link type'), max_length=10, choices=LINK_TYPES)
    url = models.URLField(_('URL'), max_length=200, null=True, blank=True)
    title = models.CharField(_('title'), max_length=200, null=True, blank=True)
    description = models.TextField(_('description'), null=True, blank=True)

    order = models.PositiveIntegerField()

    def __str__(self):
        return self.title

    class Meta(object):
        verbose_name = _('design link')
        verbose_name_plural = _('design links')
        ordering = ('order', 'id')
