"""Admin for designs application."""

from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from django.utils.translation import ugettext as _
from pagedown.widgets import AdminPagedownWidget
from sorl.thumbnail.admin import AdminImageMixin

from designs.models import (
    BoatKind,
    Design,
    Designer,
    HullConstruction,
    Image,
    Link,
    Propulsion,
    Video,
)


@admin.register(Propulsion)
class PropulsionAdmin(admin.ModelAdmin):
    """Modeladmin for propulsion."""

    list_display = ('name', 'long_name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(HullConstruction)
class HullConstructionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BoatKind)
class BoatKindAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Designer)
class DesignerAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'enabled')
    prepopulated_fields = {'slug': ('name',)}


class ImageInline(AdminImageMixin, admin.TabularInline):
    model = Image
    extra = 0
    sortable = 'order'


class VideoInline(AdminImageMixin, admin.TabularInline):
    model = Video
    extra = 0
    sortable = 'order'


class LinkInline(AdminImageMixin, admin.TabularInline):
    model = Link
    extra = 0
    sortable = 'order'


@admin.register(Design)
class DesignAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('name', 'designer', 'propulsion', 'score', 'view_on_site')
    list_filter = ('designer', 'propulsion')
    search_fields = ('name',)
    inlines = [ImageInline, VideoInline, LinkInline]
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('kinds', 'hull_constructions', 'see_also', 'tags')
    ordering = ('-id',)
    formfield_overrides = {
        models.TextField: {'widget': AdminPagedownWidget},
    }
    fieldsets = (
        (
            _('Design info'),
            {
                'fields': (
                    ('name', 'slug'),
                    'tiny_description',
                    'designer',
                    'url',
                    'tags',
                    'propulsion',
                    'kinds',
                ),
            },
        ),
        (
            _('Meta info'),
            {
                'fields': ('meta_description', 'meta_keywords'),
                'classes': ('collapse',),
            },
        ),
        (
            _('Construction'),
            {
                'fields': ('hull_type', 'hull_constructions'),
            },
        ),
        (
            _('Dimensions'),
            {
                'fields': (
                    ('loa', 'lod'),
                    'lwl',
                    ('beam', 'bwl'),
                    ('draft', 'draft_cb_up'),
                    ('depth', 'freeboard'),
                    'weight',
                    ('ballast_weight', 'cb_weight'),
                    ('displacement', 'capacity'),
                ),
            },
        ),
        (
            _('Sails & engine'),
            {
                'fields': (
                    'sail_area',
                    ('sail_area_main', 'sail_area_jib'),
                    ('sail_area_genoa', 'sail_area_spi'),
                    ('horsepower', 'engine_type'),
                ),
            },
        ),
        (
            _('Accommodation'),
            {
                'fields': ('headroom', ('accommodation', 'berths')),
            },
        ),
        (
            _('Description'),
            {
                'fields': ('description', 'image'),
            },
        ),
        (
            _('Pricing, lang'),
            {
                'fields': (('price', 'kit_price'), 'lang'),
            },
        ),
        (
            None,
            {'fields': ('see_also', 'enabled')},
        ),
    )

    def view_on_site(self, design):
        """Link to design's page."""
        return format_html('<a href="{0}">View</a>', design.get_absolute_url())
