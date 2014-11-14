from django.contrib import admin
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.conf import settings

from apps.accounts.forms import LoginForm

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$',
        'django.contrib.auth.views.login',
        {'authentication_form': LoginForm},
        name='login'),

    url(r'^logout/',
        'django.contrib.auth.views.logout',
        {'next_page': '/'},
        name='logout'),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
