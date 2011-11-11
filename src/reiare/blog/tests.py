# -*- coding: utf-8 -*-
#from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from reiare.blog.models import *


class ReiareExtrasTestCase(TestCase):

    def setUp(self):
        self.body = u'<pre class="code">\n<code class="xml">\n&lt;script src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.3/jquery.min.js"&gt;&lt;/script&gt;\n&lt;script src="/{ 任意のパス }/jquery.lazyload.mini.js"&gt;&lt;/script&gt;\n</code>\n</pre>'
        self.regex_string = '<pre.*?</pre>'

    def test_remove_linebreaks_using_regex(self):
        from django.template import defaultfilters
        from blog.templatetags import reiare_extras
        self.assertEquals(reiare_extras.remove_linebreaks_using_regex(defaultfilters.linebreaks(self.body),
                                                                      self.regex_string),
                          '<p>' + self.body + '</p>')


class BaseResponseTestCase(TestCase):

    def responseFromClientAndURL(self, client, url, data={}, status_code=200):
        response = client.get(url, data)
        self.statusCodeTest(response, status_code)
        return response

    def statusCodeTest(self, response, status_code=200):
        self.assertEqual(response.status_code, status_code)

    def statusCodeTestFromClientAndURL(self, client, url, data={}, status_code=200):
        self.responseFromClientAndURL(client, url, data, status_code)

    def templatesTest(self, names, response):
        for i in range(len(response.templates)):
            self.assertEqual(response.templates[i].name, names[i])

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
        self.simplifyResponseTest(self.client, '/blog/',
                                  templates=('2.0/generic/entry_archive.html',
                                             '2.0/base.html',
                                             '2.0/generic/entry_archive_partial.html',
                                             '2.0/entry.html',
                                             '2.0/jquery_templates.html',
                                             '2.0/entry_article_template.html',
                                             '2.0/common_js.html'))

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
                'templates': ('2.0/generic/entry_archive_partial.html',
                              '2.0/entry.html')},
                {'url': '/blog/2010/11/1/',
                 'templates': ('2.0/generic/entry_archive_month_partial.html',
                               '2.0/generic/entry_archive_month_nav.html',
                               '2.0/generic/entry_archive_partial.html',
                               '2.0/entry.html',
                               '2.0/generic/entry_archive_month_nav.html')},
                {'url': '/blog/2010/11/',
                 'templates': ('2.0/generic/entry_archive_month_partial.html',
                               '2.0/generic/entry_archive_month_nav.html',
                               '2.0/generic/entry_archive_partial.html',
                               '2.0/entry.html',
                               '2.0/generic/entry_archive_month_nav.html')},
                {'url': '/blog/2010/11/05/slug/',
                 'templates': ('2.0/entry.html',)},
                {'url': '/blog/recents/1/',
                 'templates': ('2.0/generic/entry_archive_partial.html',
                               '2.0/entry.html')},
                {'url': '/blog/archives/',
                 'templates': ('2.0/archive_partial.html',)})
        for arg in args:
            self.simplifyPjaxResponseTest(self.client, arg['url'], templates= arg['templates'])


    def testFeeds(self):
        response = self.client.get('/blog/feeds/latest/', follow=True)
        self.assertEqual(response.redirect_chain[1][1], 302)
        self.assertEqual(response.redirect_chain[0][0], 'http://feeds.feedburner.com/reiare/cPIq')
        self.simplifyResponseTest(self.client, '/blog/feeds/tag/apple/',
                                  templates=('feeds/tag_title.html',
                                             'feeds/tag_description.html'))
        self.simplifyResponseTest(self.client, '/blog/feeds_ad/latest/', {},
                                  templates=('feeds/latest_title.html',
                                             'feeds/latest_description.html'))

    def testOldBlog(self):
        args = ({'url': '/blog/1.0/',
                 'templates': ('blog/entry_archive.html',
                               'base.html',
                               'entry.html',
                               'recent_entries_box.html')},
                {'url': '/blog/1.0/2010/10/',
                 'templates': ('blog/entry_archive_month.html',
                               'base.html',
                               'month_navigation.html',
                               'month_navigation.html',
                               'recent_entries_box.html')},
                {'url': '/blog/1.0/2010/11/05/slug/',
                 'templates': ('blog/entry_detail.html',
                               'base.html',
                               'entry.html',
                               'recent_entries_box.html')},
                {'url': '/blog/1.0/tag/apple/',
                 'templates': ('blog/entry_list.html',
                               'list_template.html',
                               'base.html',
                               'recent_entries_box.html')},
                {'url': '/blog/body/1/',
                 'templates': ('entry_body.html',
                               'entry_comment.html')},
                {'url': '/blog/recent_entries/1/',
                 'templates': ('recent_entries_box.html',)},
                {'url': '/blog/more_entries/1/',
                 'templates': ('more_entries.html',
                               'entry.html')})
        for arg in args:
            self.simplifyResponseTest(self.client, arg['url'], templates=arg['templates'])

    def testTouch(self):
        args = ({'url': '/blog/touch/',
                 'templates': ('iui_base.html',
                               'iui_entry_box.html',
                               'iui_entry_comment_box.html')},
                {'url': '/blog/touch/more_entries/1/',
                 'templates': ('iui_more_entries.html',)},
                {'url': '/blog/touch/2010/11/05/slug/',
                 'templates': ('iui_entry.html',
                               'iui_entry_box.html',
                               'iui_entry_comment_box.html')},
                {'url': '/blog/touch/tag/test/',
                 'templates': ('iui_entries_by_tag.html',)},
                {'url': '/blog/touch/tag/1/',
                 'templates': ('iui_entries_by_tag.html',)},
                {'url': '/blog/touch/tag/test/more_entries/1/',
                 'templates': ('iui_more_entries.html',)})
        for arg in args:
            self.simplifyResponseTest(self.client, arg['url'], templates=arg['templates'])

    def testAsin2Asamashi(self):
        self.responseFromClientAndURL(self.client, 'http://reiare.net/blog/asin2asamashi/spiceoflife04-22/B005119CMA/')

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



