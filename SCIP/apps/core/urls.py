from django.conf.urls import patterns, url

from apps.core.views import SimpleStaticView
from django.views.generic import TemplateView

urlpatterns = patterns(
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^(?P<url>\w+)$', TemplateView.as_view(template_name='index.html'), name='urls'),
    url(r'_partials/(?P<template_name>\w+)$', SimpleStaticView.as_view(), name='partials'),
    )
