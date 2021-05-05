"""Designs API URL Configuration."""
from django.urls import path

from designs.api import views

urlpatterns = [
    path('site-info/', views.site_info),
]
