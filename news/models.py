"""Models for news application."""

from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from sorl.thumbnail import ImageField

from designs.models import Design


class News(models.Model):
    """News article."""

    title = models.CharField(_('title'), max_length=150)
    slug = models.SlugField(_('slug'), max_length=150, db_index=True)
    image = ImageField(
        _('image'),
        upload_to='news/%Y/%m',
        max_length=250,
        help_text=_('~400x300px'),
    )
    content = models.TextField(_('content'), help_text=_('valid HTML, please'))  # noqa: WPS110
    url = models.URLField(
        _('URL'),
        max_length=250,
        null=True,
        blank=True,
        help_text=_('if any'),
    )

    designs = models.ManyToManyField(Design, blank=True, verbose_name=_('mentioned designs'))

    enabled = models.BooleanField(_('enabled'), default=True)
    created_at = models.DateTimeField(db_index=True, editable=False, default=now)

    class Meta(object):
        verbose_name = _('news')
        verbose_name_plural = _('news')
        ordering = ('-created_at',)

    def __str__(self):
        return self.title
