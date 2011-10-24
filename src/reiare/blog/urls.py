# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url
from django.views.decorators.cache import cache_page
from django.views.generic.dates import ArchiveIndexView

from blog.apis import EntryMonthArchiveView, MonthArchiveView2
from blog.models import Entry
from blog.feeds import LatestEntries, LatestEntriesByTag


feeds = {
    'latest': LatestEntries,
    'tags': LatestEntriesByTag,
    'tag': LatestEntriesByTag
}

urlpatterns = patterns('blog.views',
    (r'^tag/(?P<tag>.*)/image/$', 'tag_image_list'),
    (r'^1.0/tag/(?P<tag>.*)/$', 'tag_list'),
    (r'^1.0/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>.*)/$', 'detail'),
    (r'^asin2asamashi/(?P<associate_tag>.*)/(?P<asins>.*)/$', 'asin2asamashi'),
    (r'^body/(?P<object_id>\d+)/$', 'get_body'),
    (r'^recent_entries/(?P<page_num>\d+)/$', 'get_recent_entries'),
    (r'^more_entries/(?P<page_num>\d+)/$', 'get_more_entries'),
    (r'^touch/$', 'get_iui_page'),
    (r'^touch/more_entries/(?P<page_num>\d+)/$', 'get_iui_more_entries'),
    (r'^touch/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>.*)/$', 'get_iui_entry'),
    (r'^touch/tag/(?P<tag>.*)/more_entries/(?P<page_num>\d+)/$', 'get_iui_more_entries_by_tag'),
    (r'^touch/tag/(?P<tag>.*)/$', 'get_iui_entries_by_tag'),
    (r'^touch/tag/(?P<tag>.*)/(?P<page_num>\d+)/$', 'get_iui_entries_by_tag'),
    (r'^touch/post_comment/(?P<object_id>\d+)/$', 'post_iui_entry_comment'),
)

urlpatterns += patterns('',
    (r'^1.0/$', ArchiveIndexView.as_view(
        queryset=Entry.published_objects.all().select_related(),
        date_field='created',
        paginate_by=5)),
    (r'^1.0/(?P<year>\d{4})/(?P<month>\d{2})/$', EntryMonthArchiveView.as_view()),
    # url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', cache_page(MonthArchiveView2.as_view(), 86400),
    #     name='archive_month'),
)

urlpatterns += patterns('',
                        (r'^feeds/latest/$',
                         'blog.apis.feeds_latest_redirect',
                         ),
                        url(r'^feeds/(?P<url>.*)/$',
                            'django.contrib.syndication.views.feed',
                            {'feed_dict': feeds},
                            'blog_feeds'),
                        url(r'^feeds_ad/(?P<url>.*)/$',
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
                        (r'^tag/(?P<tag>.*)/(?P<page>\d+)/$', 'tag_entries_index_pjax'),
                        (r'^tag/(?P<tag>.*)/$', 'tag_entries_index_pjax'),
                        url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<page>\d+)/$', 'archive_month_pjax'),
                        url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$', 'archive_month_pjax'),
                        (r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>.*)/$', 'detail_pjax'),
                        (r'^recents/(?P<page>\d)/$', 'index_pjax'),
                        (r'^archives/$', 'archives_pjax'),
                        (r'^mobile/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>.*)/$', 'mobile_detail'),
                        (r'^mobile/(?P<year>\d{4})/(?P<month>\d{2})/(?P<page>\d+)/$', 'mobile_month'),
                        (r'^mobile/(?P<year>\d{4})/(?P<month>\d{2})/$', 'mobile_month'),
                        (r'^mobile/archives/(?P<year>\d{4})/$', 'mobile_archive_year'),
                        (r'^mobile/archives/$', 'mobile_archive_index'),
                        (r'^mobile/tag/(?P<tag>.*)/(?P<page>\d+)/$', 'mobile_tag'),
                        (r'^mobile/tag/(?P<tag>.*)/$', 'mobile_tag'),
                        (r'^mobile/tag/$', 'mobile_tag_index'),
                        (r'^mobile/recents/(?P<page>\d+)/$', 'mobile_index'),
                        (r'^mobile/$', 'mobile_index'),
                        (r'^qunit/$', 'qunit'),
                        (r'^$', 'index_pjax'),
                        )
