from django.conf.urls import patterns, include, url

from apps.api.views import *


users_urls = patterns(
    '',
    url(r'^(/)?$', UsersView.as_view(), name="user_list"),

    url(r'^/(?P<username>[0-9a-zA-Z_-]+)/workdays/last(/)?$', UserLastWorkdayView.as_view(), name="user_last_workday"),
    url(r'^/(?P<username>[0-9a-zA-Z_-]+)/workdays(/)?$', UserWorkdaysView.as_view(), name="user_workday_list"),
    url(r'^/(?P<username>[0-9a-zA-Z_-]+)(/)?$', SpecificUserView.as_view(), name="user_detail"),

)

workdays_urls = patterns(
    '',
    url(r'^(/)?$', WorkdaysView.as_view(), name="workday_list"),
    url(r'^/(?P<pk>[0-9]+)(/)?$', SpecificWorkdayView.as_view(), name="workday_detail"),
)

urlpatterns = patterns(
    '',
    url(r'^users', include(users_urls)),
    url(r'^workdays', include(workdays_urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
)
