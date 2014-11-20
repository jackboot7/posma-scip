from django.contrib import admin
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.conf import settings


admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^v1/', include('apps.api.urls'))
)

if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
