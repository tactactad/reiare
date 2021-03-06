# -*- coding: utf-8 -*-

import json
import logging

#from django.contrib.auth.models import User
from django.http import Http404
from django.template import defaultfilters
from django.test import TestCase
from django.test.client import Client

from blog import apis
from blog.models import *
from blog.templatetags import reiare_extras
from blog.templatetags import blog_tag_extras

class ReiareExtrasTestCase(TestCase):

    def setUp(self):
        self.body = u'<pre class="code">\n<code class="xml">\n&lt;script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.3/jquery.min.js"&gt;&lt;/script&gt;\n&lt;script src="/{ 任意のパス }/jquery.lazyload.mini.js"&gt;&lt;/script&gt;\n</code>\n</pre>'
        self.regex_string = '<pre.*?</pre>'

    def test_remove_linebreaks_using_regex(self):
        self.assertEquals(reiare_extras.remove_linebreaks_using_regex(defaultfilters.linebreaks(self.body),
                                                                      self.regex_string),
                          '<p>' + self.body + '</p>')

    def testOmit(self):
        value = '123456789abcdef'
        self.assertEqual(reiare_extras.omit(value, 2), u'1234567\u2026ef')
        self.assertEqual(reiare_extras.omit(value, 15), value)
        self.assertEqual(reiare_extras.omit(value), value)
        self.assertEqual(reiare_extras.omit(value, 11), u'12345678\u2026ef')

    def testWrappedJQueryTemplatetag(self):
        value = '123456789'
        self.assertEqual(reiare_extras.wrapped_jQuery_templatetag(value), u'{{123456789}}')

    def testRewriteImgSrc(self):
        value = 'spam<img src="/site_media/ham">egg'
        self.assertEqual(reiare_extras.rewrite_img_src(value),
                         u'spam<img src="http://reiare.net/site_media/ham">egg')

    def testRewriteAHref(self):
        value = 'spma<a href="/blog/ham">egg</a>'
        self.assertEqual(reiare_extras.rewrite_a_href(value),
                         u'spma<a href="http://reiare.net/blog/ham">egg</a>')


class BlogTagExtrasTestCase(TestCase):
    fixtures = ['entryTag.json', 'entry.json', 'user.json']

    def setUp(self):
        pass

    def testShowRecentEntries(self):
        dict = blog_tag_extras.show_recent_entries()
        self.assertTrue(isinstance(dict['entries'][0], Entry))

    def testShowRandomEntries(self):
        dict = blog_tag_extras.show_random_entries()
        self.assertTrue(isinstance(dict['entries'].pop(), Entry))

    def testShowTags(self):
        dict = blog_tag_extras.show_tags()
        self.assertTrue(isinstance(dict['tags'][0], EntryTag))

    def tearDown(self):
        pass


class ApiTestCase(TestCase):
    fixtures = ['entry.json', 'entryTag.json', 'entryArchive.json', 'user.json']

    def setUp(self):
        self.entries = Entry.objects.all()
        self.tags = EntryTag.objects.all()
        self.archives = EntryArchive.objects.all()

    def testTitleJson(self):
        data = json.loads(apis.title_json_from_entries(self.entries))
        self.assertEqual(data[0]['title'], 'fixture1')
        self.assertEqual(data[0]['url'], '/blog/2011/11/06/fixture1/')

    def testJsonSourceFromEntries(self):
        data = apis.json_source_from_entries(self.entries)
        self.assertEqual(data[0]['body'], '<p>fixture1 body</p>')
        self.assertEqual(data[0]['display_created'], u'2011/11/6 (\u65e5) p.m.02:50')
        self.assertEqual(data[0]['rel_entries'][0]['id'], 2)
        self.assertEqual(data[0]['tags'][0]['name'], 'apple')

    def testJsonSourceFromTags(self):
        data = apis.json_source_from_tags(self.tags)
        self.assertEqual(data[0]['id'], 1)
        self.assertEqual(data[0]['url'], '/blog/tag/apple/')

    def testJsonSourceFromArchives(self):
        data = apis.json_source_from_archives(self.archives)
        self.assertEqual(data[0]['url'], '/blog/2010/10/')

    def testJsonFromEntries(self):
        data = json.loads(apis.json_from_entries(self.entries))
        self.assertEqual(data[0]['body'], '<p>fixture1 body</p>')
        self.assertEqual(data[0]['display_created'], u'2011/11/6 (\u65e5) p.m.02:50')
        self.assertEqual(data[0]['rel_entries'][0]['id'], 2)
        self.assertEqual(data[0]['tags'][0]['name'], 'apple')

    def testJsonFromTags(self):
        data = json.loads(apis.json_from_tags(self.tags))
        self.assertEqual(data[0]['id'], 1)
        self.assertEqual(data[0]['url'], '/blog/tag/apple/')

    def testRecentEntriesFromNumAndPage(self):
        data = apis.recent_entries_from_num_and_page(10, 2)
        self.assertEqual(data[0].title, 'fixture11')

    def testRandomEntriesFromNum(self):
        data = apis.random_entries_from_num(5)
        self.assertEqual(len(data), 5)
        self.assertTrue(isinstance(data.pop(), Entry))

    def testJsonResponse(self):
        response = apis.json_response('[]')
        self.assertEqual(response.__getitem__('CONTENT-TYPE'), 'application/json')

    def testPaginatorFromObjectsAndNumAndPage(self):
        data = apis.paginator_from_objects_and_num_and_page(self.entries, 5, 2)
        self.assertTrue(data[0]['has_next'])
        self.assertTrue(data[0]['has_previous'])
        self.assertEqual(data[0]['next_page_number'], 3)
        self.assertEqual(data[1][0].title, 'fixture6')
        self.assertEqual(data[1][4].title, 'fixture10')

    def testEntriesFromSlug(self):
        data = apis.entries_from_slug(2011, 11, 6, 'fixture1')
        self.assertEqual(data[0].title, 'fixture1')
#        self.assertRaises(Http404, apis.entries_from_slug(2011, 11, 6, 'dummy'))

    def testEntriesFromYearAndMonth(self):
        data = apis.entries_from_year_and_month(2011, 11)
        self.assertEqual(data[0].title, 'fixture1')

    def tearDown(self):
        pass


class BaseResponseTestCase(TestCase):

    def responseFromClientAndURL(self, client, url, data={}, status_code=200):
        response = client.get(url, data)
        self.statusCodeTest(response, status_code)
        return response

    def statusCodeTest(self, response, status_code=200):
        self.assertEqual(response.status_code, status_code, msg='errored url is %s' % (response.request['PATH_INFO']))

    def statusCodeTestFromClientAndURL(self, client, url, data={}, status_code=200):
        self.responseFromClientAndURL(client, url, data, status_code)

    def templatesTest(self, names, response):
        for i in range(len(response.templates)):
            self.assertEqual(response.templates[i].name, names[i], msg='errored url is %s(%s != %s)' % (response.request['PATH_INFO'], response.templates[i].name, names[i]))

    def simplifyResponseTest(self, client, url, data={}, templates=(), status_code=200):
        response = self.responseFromClientAndURL(client, url, data, status_code)
        self.templatesTest(templates, response)

    def simplifyPjaxResponseTest(self, client, url, data={}, templates=(), status_code=200):
        response = client.get(url, data, HTTP_X_PJAX=True)
        self.statusCodeTest(response, status_code)
        self.templatesTest(templates, response)

    def jsonResponseTest(self, client, url, data={}, status_code=200):
        response = client.get(url, data,
                              HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.statusCodeTest(response, status_code)
        self.assertEqual(response['Content-TYpe'], 'application/json')


class ResponseTestCase(BaseResponseTestCase):

    def setUp(self):
        self.user, flag = User.objects.get_or_create(username='testuser')
        self.user.set_password('testpass')
        self.user.save()
        self.entry, flag = Entry.objects.get_or_create(title=u'タイトル', body=u'本文', slug='slug',
                                                  created=datetime.datetime(2010, 11, 5, 17, 7, 16),
                                                  created_by=self.user, is_publish=True)
        self.tag, flag = EntryTag.objects.get_or_create(name=u'apple')
        self.client = Client()

    def testblog(self):
        args = ({'url': '/blog/',
                 'templates': ('2.0/generic/entry_archive.html',
                               '2.0/base.html',
                               '2.0/generic/entry_archive_partial.html',
                               '2.0/entry.html',
                               '2.0/entry.html',
                               '2.0/entry.html',
                               '2.0/entry.html',
                               '2.0/jquery_templates.html',
                               '2.0/entry_article_template.html',
                               '2.0/common_js.html')},
                {'url': '/blog/2010/11/1/',
                 'templates': ('2.0/generic/entry_archive_month.html',
                               '2.0/base.html',
                               '2.0/generic/entry_archive_month_partial.html',
                               '2.0/generic/entry_archive_month_nav.html',
                               '2.0/generic/entry_archive_partial.html',
                               '2.0/entry.html',
                               '2.0/entry.html',
                               '2.0/generic/entry_archive_month_nav.html',
                               '2.0/jquery_templates.html',
                               '2.0/entry_article_template.html',
                               '2.0/common_js.html')},
                {'url': '/blog/2010/11/',
                 'templates': ('2.0/generic/entry_archive_month.html',
                               '2.0/base.html',
                               '2.0/generic/entry_archive_month_partial.html',
                               '2.0/generic/entry_archive_month_nav.html',
                               '2.0/generic/entry_archive_partial.html',
                               '2.0/entry.html',
                               '2.0/entry.html',
                               '2.0/generic/entry_archive_month_nav.html',
                               '2.0/jquery_templates.html',
                               '2.0/entry_article_template.html',
                               '2.0/common_js.html')},
                {'url': '/blog/2010/11/05/slug/',
                 'templates': ('2.0/generic/entry_archive.html',
                               '2.0/base.html',
                               '2.0/generic/entry_archive_partial.html',
                               '2.0/entry.html',
                               '2.0/entry.html',
                               '2.0/jquery_templates.html',
                               '2.0/entry_article_template.html',
                               '2.0/common_js.html')},
                {'url': '/blog/recents/1/',
                 'templates': ('2.0/generic/entry_archive.html',
                               '2.0/base.html',
                               '2.0/generic/entry_archive_partial.html',
                               '2.0/entry.html',
                               '2.0/entry.html',
                               '2.0/entry.html',
                               '2.0/entry.html',
                               '2.0/jquery_templates.html',
                               '2.0/entry_article_template.html',
                               '2.0/common_js.html')},
                {'url': '/blog/archives/',
                 'templates': ('2.0/archives.html',
                               '2.0/base.html',
                               '2.0/archive_partial.html',
                               '2.0/jquery_templates.html',
                               '2.0/entry_article_template.html',
                               '2.0/common_js.html')})
        for arg in args:
            self.simplifyResponseTest(self.client, arg['url'], templates= arg['templates'])

    def testRecentJson(self):
        self.responseFromClientAndURL(self.client, '/blog/api/recents/1/entry.json', status_code=302)
        self.jsonResponseTest(self.client, '/blog/api/recents/1/entry.json')

    def testApi(self):
        for url in ('/blog/api/2010/11/05/slug/entry.json',
                    '/blog/api/2010/11/1/entry.json',
                    '/blog/api/2010/11/entry.json',
                    '/blog/api/entry/1.json',
                    '/blog/api/recents/1/entry.json',
                    '/blog/api/recents/title.json',
                    '/blog/api/random/title.json',
                    '/blog/api/archives/title.json',
                    '/blog/api/tag/apple/1/entry.json',
                    '/blog/api/tag/apple/entry.json',
                    '/blog/api/tag/apple/entry.json'):
            self.jsonResponseTest(self.client, url)
        # urls = ['/blog/api/2010/11/05/slug/entry.json',
        #         '/blog/api/2010/11/1/entry.json',
        #         '/blog/api/2010/11/entry.json',
        #         '/blog/api/entry/1.json',
        #         '/blog/api/recents/1/entry.json',
        #         '/blog/api/recents/title.json',
        #         '/blog/api/random/title.json',
        #         '/blog/api/archives/title.json',
        #         '/blog/api/tag/apple/1/entry.json',
        #         '/blog/api/tag/apple/entry.json',
        #         '/blog/api/tag/apple/entry.json']
        # map((lambda url: self.jsonResponseTest(self.client, url)), urls)

    def testPjax(self):
        args = ({'url': '/blog/',
                'templates': (
                    '2.0/generic/entry_archive_partial.html',
                    '2.0/entry.html',
                    '2.0/entry.html',
                    '2.0/entry.html',
                    '2.0/entry.html')},
                {'url': '/blog/2010/11/1/',
                 'templates': ('2.0/generic/entry_archive_month_partial.html',
                               '2.0/generic/entry_archive_month_nav.html',
                               '2.0/generic/entry_archive_partial.html',
                               '2.0/entry.html',
                               '2.0/entry.html',
                               '2.0/generic/entry_archive_month_nav.html')},
                {'url': '/blog/2010/11/',
                 'templates': ('2.0/generic/entry_archive_month_partial.html',
                               '2.0/generic/entry_archive_month_nav.html',
                               '2.0/generic/entry_archive_partial.html',
                               '2.0/entry.html',
                               '2.0/entry.html',
                               '2.0/generic/entry_archive_month_nav.html')},
                {'url': '/blog/2010/11/05/slug/',
                 'templates': ('2.0/entry.html',)},
                {'url': '/blog/recents/1/',
                 'templates': ('2.0/generic/entry_archive_partial.html',
                               '2.0/entry.html',
                               '2.0/entry.html',
                               '2.0/entry.html',
                               '2.0/entry.html')},
                {'url': '/blog/archives/',
                 'templates': ('2.0/archive_partial.html',)})
        for arg in args:
            self.simplifyPjaxResponseTest(self.client, arg['url'], templates= arg['templates'])


    def testFeeds(self):
        response = self.client.get('/blog/feeds/latest/', follow=True)
        # self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.redirect_chain[0][0], 'http://feeds.feedburner.com/reiare/cPIq')
#         self.simplifyResponseTest(self.client, '/blog/feeds/tag/apple/',
#                                   templates=('feeds/tag_title.html',
#                                              'feeds/tag_description.html'))
#         self.simplifyResponseTest(self.client, '/blog/feeds_ad/latest/', {},
#                                   templates=('feeds/latest_title.html',
#                                              'feeds/latest_description.html'))

    def testMobile(self):
        args = [{'url': '/blog/mobile/2010/11/05/slug/',
                 'templates': ('2.0/mobile/mobile_detail.html',
                               '2.0/mobile/mobile_base.html')},
                {'url': '/blog/mobile/2010/11/1/',
                 'templates': ('2.0/mobile/mobile_archive.html',
                               '2.0/mobile/mobile_base.html',
                               '2.0/mobile/mobile_entry_li.html',
                               '2.0/mobile/mobile_entry_li.html',
                               '2.0/mobile/mobile_paginator.html')},
                {'url': '/blog/mobile/2010/11/',
                 'templates': ('2.0/mobile/mobile_archive.html',
                               '2.0/mobile/mobile_base.html',
                               '2.0/mobile/mobile_entry_li.html',
                               '2.0/mobile/mobile_entry_li.html',
                               '2.0/mobile/mobile_paginator.html')},
                {'url': '/blog/mobile/archives/2010/',
                 'templates': ('2.0/mobile/mobile_archives_year.html',
                               '2.0/mobile/mobile_base.html')},
                {'url': '/blog/mobile/archives/',
                 'templates': ('2.0/mobile/mobile_archives.html',
                               '2.0/mobile/mobile_base.html')},
                {'url': '/blog/mobile/tag/apple/1/',
                 'templates': ('2.0/mobile/mobile_tag.html',
                               '2.0/mobile/mobile_base.html',
                               '2.0/mobile/mobile_paginator.html')},
                {'url': '/blog/mobile/tag/apple/',
                 'templates': ('2.0/mobile/mobile_tag.html',
                               '2.0/mobile/mobile_base.html',
                               '2.0/mobile/mobile_paginator.html')},
                {'url': '/blog/mobile/tag/',
                 'templates': ('2.0/mobile/mobile_tags.html',
                               '2.0/mobile/mobile_base.html')},
                {'url': '/blog/mobile/recents/1/',
                 'templates': ('2.0/mobile/mobile_index.html',
                               '2.0/mobile/mobile_base.html',
                               '2.0/mobile/mobile_entry_li.html',
                               '2.0/mobile/mobile_entry_li.html',
                               '2.0/mobile/mobile_entry_li.html',
                               '2.0/mobile/mobile_entry_li.html',
                               '2.0/mobile/mobile_paginator.html',)},
                {'url': '/blog/mobile/',
                 'templates': ('2.0/mobile/mobile_index.html',
                               '2.0/mobile/mobile_base.html',
                               '2.0/mobile/mobile_entry_li.html',
                               '2.0/mobile/mobile_entry_li.html',
                               '2.0/mobile/mobile_entry_li.html',
                               '2.0/mobile/mobile_entry_li.html',
                               '2.0/mobile/mobile_paginator.html')},]
        for arg in args:
            self.simplifyResponseTest(self.client, arg['url'], templates=arg['templates'])

#     def testOldBlog(self):
#         args = ({'url': '/blog/1.0/',
#                  'templates': ('blog/entry_archive.html',
#                                'base.html',
#                                'entry.html',
#                                'entry.html',
#                                'entry.html',
#                                'entry.html',
#                                'recent_entries_box.html')},
#                 {'url': '/blog/1.0/2010/10/',
#                  'templates': ('blog/entry_archive_month.html',
#                                'base.html',
#                                'month_navigation.html',
#                                'month_navigation.html',
#                                'recent_entries_box.html')},
#                 {'url': '/blog/1.0/2010/11/05/slug/',
#                  'templates': ('blog/entry_detail.html',
#                                'base.html',
#                                'entry.html',
#                                'recent_entries_box.html')},
#                 {'url': '/blog/1.0/tag/apple/',
#                  'templates': ('blog/entry_list.html',
#                                'list_template.html',
#                                'base.html',
#                                'recent_entries_box.html')},
#                 {'url': '/blog/body/1/',
#                  'templates': ('entry_body.html',
#                                'entry_comment.html')},
#                 {'url': '/blog/recent_entries/1/',
#                  'templates': ('recent_entries_box.html',)},
#                 {'url': '/blog/more_entries/1/',
#                  'templates': ('more_entries.html',
#                                'entry.html')})
#         for arg in args:
#             self.simplifyResponseTest(self.client, arg['url'], templates=arg['templates'])

#     def testTouch(self):
#         args = ({'url': '/blog/touch/',
#                  'templates': ('iui_base.html',
#                                'iui_entry_box.html',
#                                'iui_entry_comment_box.html')},
#                 {'url': '/blog/touch/more_entries/1/',
#                  'templates': ('iui_more_entries.html',)},
#                 {'url': '/blog/touch/2010/11/05/slug/',
#                  'templates': ('iui_entry.html',
#                                'iui_entry_box.html',
#                                'iui_entry_comment_box.html')},
#                 {'url': '/blog/touch/tag/test/',
#                  'templates': ('iui_entries_by_tag.html',)},
#                 {'url': '/blog/touch/tag/1/',
#                  'templates': ('iui_entries_by_tag.html',)},
#                 {'url': '/blog/touch/tag/test/more_entries/1/',
#                  'templates': ('iui_more_entries.html',)})
#         for arg in args:
#             self.simplifyResponseTest(self.client, arg['url'], templates=arg['templates'])

#     def testAsin2Asamashi(self):
#         self.responseFromClientAndURL(self.client, 'http://reiare.net/blog/asin2asamashi/spiceoflife04-22/B005119CMA/')

    def testAdmin(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client.login(username='testuser', password='testpass'))

    def tearDown(self):
        self.entry.delete()
        self.tag.delete()

# class EntryArchiveTestCase(TestCase):
#     fixtures = ['fortest.yaml',]#'entryArchive.json',]
# #                'asamashiRakutenGenreXML.yaml']

#     def setUp(self):
#          self.obj, self.flg = EntryArchive.objects.get_or_create(yearmonth='200909')

#     def testGetter(self):
#         #print 'unit testGetter'
#         self.assertEquals(self.obj._month(), '09')
#         self.assertEquals(self.obj._year(), '2009')

#     def testFluffyGetter(self):
#         #print 'unit testFluffyGetter'
#         obj = EntryArchive.objects.get(id=1)
#         self.assertEquals(obj._month(), '09')
#         self.assertEquals(obj.get_absolute_url(), '/blog/2009/09/')

# class EntryTagTestCase(TestCase):
#     def setUp(self):
#         self.ea = EntryArchive.objects.get(id=1)

#     def testGetter(self):
#         self.assertEquals(self.ea.month, '09')
