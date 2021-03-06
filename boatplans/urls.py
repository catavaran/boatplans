"""boatplans URL Configuration."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('api/', include('designs.api.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar  # noqa: WPS433

        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns

    urlpatterns += static('/media/', document_root=settings.MEDIA_ROOT)


# Should be the last url pattern
# urlpatterns += [path('', include('designs.urls'))]  noqa: E800
