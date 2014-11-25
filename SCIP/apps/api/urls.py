from django.conf.urls import patterns, include, url

from apps.api.views import *


users_urls = patterns(
    '',
    url(r'^(/)?$', UsersView.as_view()),

    url(r'^/(?P<username>[0-9a-zA-Z_-]+)/workdays/last(/)?$', UserLastWorkdayView.as_view()),
    url(r'^/(?P<username>[0-9a-zA-Z_-]+)/workdays(/)?$', UserWorkdaysView.as_view()),
    url(r'^/(?P<username>[0-9a-zA-Z_-]+)(/)?$', SpecificUserView.as_view()),

)

workdays_urls = patterns(
    '',
    url(r'^(/)?$', WorkdaysView.as_view()),
    url(r'^/(?P<pk>[0-9]+)(/)?$', SpecificWorkdayView.as_view()),
)

urlpatterns = patterns(
    '',
    url(r'^users', include(users_urls)),
    url(r'^workdays', include(workdays_urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)
