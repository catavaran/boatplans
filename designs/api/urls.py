"""Designs API URL Configuration."""
from django.urls import path

from designs.api import views

urlpatterns = [
    path('site-info/', views.SiteInfoView.as_view()),
    path('designs/recent/', views.RecentDesignsView.as_view()),
]
