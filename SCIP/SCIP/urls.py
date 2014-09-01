from apps.accounts.forms import LoginForm
from apps.registro.views import RegistroView
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       #url(r'^$', include('SCIP.apps.urls'))),

                       # Uncomment to enable the admin urls.
                       #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       url(r'^$',
                           'django.contrib.auth.views.login',
                           {'authentication_form': LoginForm},
                           name='login'),

                       url(r'^logout/',
                           'django.contrib.auth.views.logout',
                           {'next_page': '/'},
                           name='logout'),

                       url(r'^registro/$', RegistroView.as_view(), name='registro'),

                       url(r'^admin/', include(admin.site.urls)),
                       )

if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
