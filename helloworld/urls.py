# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = [
    url(r'^ranking/(?P<edition>\w+)/(?P<pivot>\d+)', 'helloworld.views.index'),
    url(r'^ranking/(?P<pivot>\d+)', 'helloworld.views.index'),
    url(r'^ranking/(?P<edition>\w+)', 'helloworld.views.index'),
    url(r'^ranking', 'helloworld.views.index'),
]


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

