from django.contrib import admin
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.conf import settings

from apps.core.views import SimpleStaticView
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'v1/auth/login/', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^v1/', include('apps.api.urls')),
    # url(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^_partials/(?P<template_name>\w+)$', SimpleStaticView.as_view(), name='partials'),
    url(r'^.*$', TemplateView.as_view(template_name='index.html'), name='simple_urls'),
    #url(r'^(?P<namespace>\w+)/(?P<url>\w+)$', TemplateView.as_view(template_name='index.html'), name='namespaced_urls'),
    )


if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
