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


class ResponseTestCase(TestCase):

    def setUp(self):
        self.user, flag = User.objects.get_or_create(username='testuser')
        self.entry, flag = Entry.objects.get_or_create(title=u'タイトル', body=u'本文', slug='slug',
                                                  created=datetime.datetime(2010, 11, 5, 17, 7, 16),
                                                  created_by=self.user, is_publish=True)
        self.client = Client()

    def testblog(self):
        response = self.client.get('/blog/')
        self.failUnlessEqual(response.status_code, 200)
        self.assertEquals(response.template[0].name,
                          '2.0/generic/entry_archive.html')
        self.assertEquals(response.template[1].name,
                          '2.0/base.html')
        self.assertEquals(response.template[2].name,
                          '2.0/entry.html')

    def testRecentJson(self):
        response = self.client.get('/blog/api/recents/1/entry.json')
        self.assertEquals(response.status_code, 302)
        response = self.client.get('/blog/api/recents/1/entry.json', {},
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response['Content-Type'], 'application/json')

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

