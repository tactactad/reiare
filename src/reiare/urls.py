from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^blog/', include('reiare.blog.urls')),
#    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'^site_media/images/(?P<path>.*)$', 'serve', {'document_root': '/Users/tac/Dropbox/reiare_images/images'}),
        (r'^site_media/(?P<path>.*)$', 'serve', {'document_root': '/Users/tac/Dropbox/reiare/src/reiare/site_media'}),
        (r'^static/(?P<path>.*)$', 'serve', {'document_root': '/Users/tac/Dropbox/reiare/src/reiare/static'}),)
