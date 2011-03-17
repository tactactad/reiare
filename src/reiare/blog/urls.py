# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.conf import settings

from blog.models import Entry, EntryArchive, EntryTag
from blog.feeds import LatestEntries, LatestEntriesByTag
from blog.forms import SearchForm

info_dict = {
    'queryset': Entry.published_objects.all().select_related(),
    'date_field': 'created'
}

feeds = {
    'latest': LatestEntries,
    'tags': LatestEntriesByTag,
    'tag': LatestEntriesByTag
}

urlpatterns = patterns('blog.views',
    (r'^tag/(?P<tag>.*)/image/$', 'tag_image_list'),
    (r'^tag/(?P<tag>.*)/$', 'tag_list'),
    # (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>.*)/post_comment/$', 'post_comment'),
    (r'^1.0/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>.*)/$', 'detail'),
    (r'^comment/(?P<object_id>\d+)/$', 'get_comment'),
    # (r'^post_comment/(?P<object_id>\d+)/$', 'post_comment_ajax'),
    (r'^asin2asamashi/(?P<associate_tag>.*)/(?P<asins>.*)/$', 'asin2asamashi'),
    (r'^body/(?P<object_id>\d+)/$', 'get_body'),
    (r'^entry/preview/$', 'get_blog_preview'),
    # (r'^search/$', 'get_search_result'),
    (r'^lastfm/recent_tracks/$', 'get_lastfm_recent_tracks'),
    (r'^lastfm/recent_weekly_track_chart/$', 'get_lastfm_recent_weekly_track_chart'),
    (r'^lastfm/recent_weekly_artist_chart/$', 'get_lastfm_recent_weekly_artist_chart'),
    (r'^lastfm/top_artists/$', 'get_lastfm_top_artists'),
    (r'^lastfm/top_tracks/$', 'get_lastfm_top_tracks'),
    (r'^recent_entries/(?P<page_num>\d+)/$', 'get_recent_entries'),
    (r'^recent_comments/(?P<page_num>\d+)/$', 'get_recent_comments'),
    (r'^more_entries/(?P<page_num>\d+)/$', 'get_more_entries'),
    (r'^touch/$', 'get_iui_page'),
    (r'^touch/more_entries/(?P<page_num>\d+)/$', 'get_iui_more_entries'),
    (r'^touch/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>.*)/$', 'get_iui_entry'),
    (r'^touch/tag/(?P<tag>.*)/more_entries/(?P<page_num>\d+)/$', 'get_iui_more_entries_by_tag'),
    (r'^touch/tag/(?P<tag>.*)/$', 'get_iui_entries_by_tag'),
    (r'^touch/tag/(?P<tag>.*)/(?P<page_num>\d+)/$', 'get_iui_entries_by_tag'),
    (r'^touch/post_comment/(?P<object_id>\d+)/$', 'post_iui_entry_comment'),
)

urlpatterns += patterns('django.views.generic.date_based',
    (r'^1.0/$', 'archive_index', dict(info_dict, num_latest=5,
                                  extra_context = {
                                      'search_form': SearchForm(),
                                  })),
    # (r'^$', 'archive_index', dict(info_dict, num_latest=5,
    #                               template_name = '2.0/generic/entry_archive.html',
    #  )),
    (r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'archive_month', dict(info_dict, month_format='%m', allow_empty=True,)),
)

urlpatterns += patterns('',
                        url(r'^feeds/(?P<url>.*)/$',
                            'django.contrib.syndication.views.feed',
                            {'feed_dict': feeds},
                            'blog_feeds'),
)

urlpatterns += patterns('blog.apis',
                        (r'^api/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>.*)/entry.json$',
                         'entry_json_from_slug'),
                        (r'^api/(?P<year>\d{4})/(?P<month>\d{2})/(?P<page>\d+)/entry.json$',
                         'archives_entries_json'),
                        (r'^api/(?P<year>\d{4})/(?P<month>\d{2})/entry.json$', 'archives_entries_json'),
                        (r'^api/entry/(?P<object_id>\d+).json$', 'entry_json'),
                        (r'^api/recents/(?P<page>\d+)/entry.json$', 'recent_entries_json'),
                        (r'^api/recents/title.json$', 'recent_entries_title_json'),
                        (r'^api/random/title.json$', 'random_entries_title_json'),
                        (r'^api/archives/title.json$', 'archives_title_json'),
                        (r'^api/tag/(?P<tag>.*)/(?P<page>\d+)/entry.json$', 'tag_entries_json'),
                        (r'^api/tag/(?P<tag>.*)/entry.json$', 'tag_entries_json'),
                        (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>.*)/$', 'detail'),
                        (r'^recents/(?P<page>\d)/$', 'index'),
                        (r'^$', 'index'),
                        )
