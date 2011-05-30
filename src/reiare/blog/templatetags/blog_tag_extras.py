# -*- coding: utf-8 -*-
import datetime
import random

from django import template

from blog.models import Entry, EntryTag


register = template.Library()


@register.inclusion_tag('2.0/recent_entries.html')
def show_recent_entries(num=10):
    return {'entries': Entry.published_objects.all()[:10]}


@register.inclusion_tag('2.0/random_entries.html')
def show_random_entries(num=10):
    if num > Entry.published_objects.count():
        num = Entry.published_objects.count()

    latest_entry = Entry.published_objects.order_by('-id')[:1].get()
    latest_entry_id = latest_entry.id
    entries = set()
    while len(entries) < num:
        entry_id = random.randint(1, latest_entry_id)
        try:
            entry = Entry.published_objects.get(id__exact=entry_id,
                                                created__lte=datetime.datetime.now())
            entries.add(entry)
        except:
            pass
    return {'entries': entries}


@register.inclusion_tag('2.0/tags.html')
def show_tags():
    return {'tags': EntryTag.objects.all()}


@register.tag(name='mobilepagerole')
def wrapped_jQueryMobile_page_role(parser, token):
    nodelist = parser.parse(('endmobilepagerole',))
    parser.delete_first_token()
    try:
        tag_name, id_value = token.split_contents()
    except ValueError:
        id_value = ''
    return WrappedJQueryMobilePageRoleNode(nodelist, id_value)

class WrappedJQueryMobilePageRoleNode(template.Node):
    def __init__(self, nodelist, id_value):
        self.nodelist = nodelist
        if id_value:
            self.id_value = template.Variable(id_value)
        else:
            self.id_value = ''

    def render(self, context):
        t = template.loader.get_template('2.0/mobile/mobile_page.html')
        context['content'] = self.nodelist.render(context)
        try:
            context['id_value'] = self.id_value.resolve(context)
        except:
            pass
        return t.render(context)
