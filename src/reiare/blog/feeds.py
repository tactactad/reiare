# -*- coding: utf-8 -*-
import datetime

from django.contrib.syndication.views import Feed
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template import defaultfilters

from blog.models import Entry, EntryTag


class LatestEntries(Feed):
    title = settings.BLOG_TITLE
    link = "/blog/"
    description = settings.BLOG_DESCRIPTION
    author_name = "tac"

    def items(self):
        return Entry.published_objects.filter(created__lte=datetime.datetime.now())[:settings.RSS_NUM]

    def item_pubdate(self, item):
        return item.created

    def item_categories(self, item):
        return [t.name for t in item.tags.all()]

    def item_link(self, obj):
        # return obj.ajax_url()
        return obj.get_absolute_url()

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.linebreaks_body_without_pre()


class LatestEntriesByTag(LatestEntries):
    description = unicode(settings.BLOG_DESCRIPTION, 'utf-8') + u"の一部"
    title_template = 'feeds/tag_title.html'
    description_template = 'feeds/tag_description.html'

    def get_object(self, response, tag):
        return get_object_or_404(EntryTag, name=tag)
        # if len(tag) != 1:
        #     raise EntryTag.ObjectDoesNotExist
        # tag = EntryTag.objects.get(name=tag)
        # return tag

    def items(self, obj):
        return Entry.published_objects.filter(tags=obj).filter(created__lte=datetime.datetime.now())[:settings.RSS_NUM]

    def title(self, obj):
        return unicode(settings.BLOG_TITLE, 'utf-8') + u"・" + obj.name

    def link(self, obj):
        return "/blog/tag/" + defaultfilters.urlencode(obj.name) + "/"
