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

    def responseFromClientAndURL(self, client, url, status_code=200):
        response = client.get(url)
        self.statusCodeTest(response, status_code)
        return response

    def statusCodeTest(self, response, status_code=200):
        self.assertEqual(response.status_code, status_code)

    def templatesTest(self, names, response):
        for i in range(len(names)):
            self.assertEqual(response.templates[i].name, names[i])


class ResponseTestCase(BaseResponseTestCase):

    def setUp(self):
        self.user, flag = User.objects.get_or_create(username='testuser')
        self.user.set_password('testpass')
        self.user.save()
        self.entry, flag = Entry.objects.get_or_create(title=u'タイトル', body=u'本文', slug='slug',
                                                  created=datetime.datetime(2010, 11, 5, 17, 7, 16),
                                                  created_by=self.user, is_publish=True)
        self.client = Client()

    def testblog(self):
        response = self.responseFromClientAndURL(self.client, '/blog/')
        self.templatesTest(['2.0/generic/entry_archive.html',
                            '2.0/base.html',
                            '2.0/generic/entry_archive_partial.html',
                            '2.0/entry.html'],
                           response)


    def testRecentJson(self):
        response = self.responseFromClientAndURL(self.client, '/blog/api/recents/1/entry.json', 302)
        response = self.client.get('/blog/api/recents/1/entry.json', {},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.statusCodeTest(response)
        self.assertEqual(response['Content-Type'], 'application/json')


    def testPjax(self):
        response = self.client.get('/blog/', {},
                                   HTTP_X_PJAX='true')
        self.statusCodeTest(response)
        self.assertEqual(response.templates[0].name,
                         '2.0/generic/entry_archive_partial.html')


    def testOldBlog(self):
        response = self.responseFromClientAndURL(self.client, '/blog/1.0/')
        self.assertEqual(response.templates[0].name,
                         'blog/entry_archive.html')


    def testAdmin(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client.login(username='testuser', password='testpass'))


    def tearDown(self):
        self.entry.delete()

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



