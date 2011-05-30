# -*- coding: utf-8 -*-
import logging
import datetime
import random
import re

from django.core import serializers
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.utils import simplejson
from django.utils.simplejson import encoder
from django.views.decorators.cache import cache_page

from blog.models import Entry, EntryArchive, EntryTag
from blog.templatetags import blog_extras


def title_json_from_entries(entries):
    data = []
    for entry in entries:
        dic = {'id': entry.id,
               'title': entry.title,
               'omitted_title': blog_extras.omit(entry.title, 23),
               'url': entry.get_absolute_url()}
        data.append(dic)
    return simplejson.dumps(data)


def json_source_from_entries(entries):
    data = []
    for entry in entries:
        rel_entries = []
        for rel_entry in entry.published_rel_entries():
            dic = {'id': rel_entry.id,
                   'title': rel_entry.title,
                   'url': rel_entry.get_absolute_url()}
            rel_entries.append(dic)

        tags = json_source_from_tags(entry.tags.all())

        dic = {'id': entry.id,
               'title': entry.title,
               'body': entry.linebreaks_body_without_pre(),
               'attr_created': entry.attr_created(),
               'display_created': entry.display_created(),
               'url': entry.get_absolute_url(),
               'tags': tags,
               'rel_entries': rel_entries}
        data.append(dic)
    return data


def json_source_from_tags(tags):
    data = []
    for tag in tags:
        dic = {'id': tag.id,
               'name': tag.name,
               'url': tag.get_absolute_url()}
        data.append(dic)
    return data


def json_source_from_archives(archives):
    data = []
    for archive in archives:
        dic = {'year': archive.year,
               'month': archive.month,
               'url': archive.get_absolute_url()}
        data.append(dic)
    return data


def json_from_entries(entries):
    return simplejson.dumps(json_source_from_entries(entries))


def json_from_tags(tags):
    return simplejson.dumps(json_source_from_tags(tags))


def recent_entries_from_num_and_page(num, page):
    start_num = (page - 1) * num
    end_num = start_num + num
    return Entry.published_objects.filter(
        created__lte=datetime.datetime.now())[start_num:end_num]


def random_entries_from_num(num):
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
    return entries


def json_response(json):
    return HttpResponse(json, mimetype='application/json')


def check_ajax_access(func):
    def inner(*args, **kwargs):
        if args[0].is_ajax():
            return func(*args, **kwargs)
        if re.match('^/blog/api/(recents|\d{4}|tag).*/entry\\.json$', args[0].path):
            url = args[0].path.replace('/blog/api/', '/blog/')
            url = url.replace('entry.json', '')
            return redirect(url)
        return HttpResponseBadRequest()
    return inner


def paginator_from_objects_and_num_and_page(objects, num, page):
    try:
        p = Paginator(objects, num)
        data = p.page(page)
    except (EmptyPage, InvalidPage):
        data = p.page(p.num_pages)
    except:
        raise Http404

    return ({'num_page': page,
             'num_pages': p.num_pages,
             'has_other_pages': data.has_other_pages(),
             'has_next': data.has_next(),
             'has_previous': data.has_previous(),
             'next_page_number': data.next_page_number(),
             'previous_page_number': data.previous_page_number(),
             'per_page': num},
            data.object_list)

def redirect_smart_phone(func):
    def inner(*args, **kwargs):
        if re.search('iPod|iPhone|Android|BlackBerry|Windows Phone|Symbian',args[0].META['HTTP_USER_AGENT']):
            return redirect(args[0].path.replace('/blog/', '/blog/mobile/'))
        return func(*args, **kwargs)
    return inner

# views
# @cache_page(86400)
# @cache_page(21600)
@redirect_smart_phone
def index(request, page=1):
    if request.GET.__contains__('_escaped_fragment_'):
        if request.GET['_escaped_fragment_'] == '' or request.GET['_escaped_fragment_'] == '/blog/':
            return redirect('/blog/')
        else:
            return redirect(request.GET['_escaped_fragment_'])

    entries = Entry.published_objects.all()
    dic, objects = paginator_from_objects_and_num_and_page(entries, 5, page)
    dic['url'] = '/blog/recents/'
    return render_to_response('2.0/generic/entry_archive.html',
                              {'latest': objects,
                               'lastupdate': objects[0].attr_created(),
                               'paginator': dic,
                               'view_mode': 'index'},
                              context_instance=RequestContext(request))

@redirect_smart_phone
def detail(request, year, month, day, slug):
    entries = Entry.published_objects.filter(created__year=year). \
        filter(created__month=month).filter(created__day=day). \
        filter(**{'slug': slug})
    return render_to_response('2.0/generic/entry_archive.html',
                              {'latest': entries,
                               'lastupdate': entries[0].attr_created(),
                               'title': entries[0].title,
                               'view_mode': 'detail'},
                              context_instance=RequestContext(request))

def tag_entries_index(request, tag, page=1):
    tag, entries = tag_and_entries(tag)
    paginator, entries = paginator_from_objects_and_num_and_page(entries, 10, page)
    return render_to_response('2.0/generic/entry_archive_tag.html',
                              {'object_list': entries,
                               'tag': tag,
                               'paginator': paginator,
                               'view_mode': 'archives'},
                              context_instance=RequestContext(request))

def tag_and_entries(tag):
    try:
        tag = EntryTag.objects.get(name__iexact=tag)
        entries = Entry.published_objects.filter(tags__name__iexact=tag).\
            filter(created__lte=datetime.datetime.now()).select_related()
    except:
        raise Http404
    return tag, entries

@check_ajax_access
def entry_json(request, object_id):
    try:
        entry = Entry.published_objects.select_related().get(pk=object_id)
    except:
        raise Http404
    dic = {'entries': json_source_from_entries([entry])}
    return json_response(simplejson.dumps(dic))


@check_ajax_access
def entry_json_from_slug(request, year, month, day, slug):
    try:
        entries = Entry.published_objects.filter(created__year=year). \
            filter(created__month=month).filter(created__day=day). \
            filter(**{'slug': slug})
    except:
        raise Http404
    return entry_json(request, entries[0].id)


@check_ajax_access
def recent_entries_json(request, page='2'):
    entries = Entry.published_objects.all()
    dic, objects = paginator_from_objects_and_num_and_page(entries, 5, page)
    json_source = {'entries': json_source_from_entries(objects),
                   'paginator': dic}
    return json_response(simplejson.dumps(json_source))


@check_ajax_access
@cache_page(21600)
def recent_entries_title_json(request, num=10, page=1):
    entries = recent_entries_from_num_and_page(num, page)
    return json_response(title_json_from_entries(entries))


@cache_page(86400)
@check_ajax_access
def random_entries_title_json(request, num=10):
    entries = random_entries_from_num(num)
    return json_response(title_json_from_entries(entries))


@check_ajax_access
@cache_page(86400)
def archives_title_json(request):
    return json_response(simplejson.dumps(json_source_from_archives(EntryArchive.objects.all())))


@check_ajax_access
@cache_page(86400)
def archives_entries_json(request, year, month, page=1):
    entries = Entry.published_objects.filter(created__year=year). \
        filter(created__month=month).order_by('created')
    paginator, objects = paginator_from_objects_and_num_and_page(entries, 10, page)
    current_archive = EntryArchive.objects.get(yearmonth=year + month);
    previous_archive = EntryArchive.objects.filter(yearmonth__lt=year + month).order_by('-yearmonth')[:1]
    next_archive = EntryArchive.objects.filter(yearmonth__gt=year+month).order_by('yearmonth')[:1]
    json_source = {'current_archive': json_source_from_archives([current_archive]),
                   'previous_archive': json_source_from_archives(previous_archive),
                   'next_archive': json_source_from_archives(next_archive),
                   'paginator': paginator,
                   'entries': json_source_from_entries(objects)}
    return json_response(simplejson.dumps(json_source))


def tag_names_json(request):
    pass


@check_ajax_access
@cache_page(86400)
def tag_entries_json(request, tag, num=10, page=1):
    tag, entries = tag_and_entries(tag)

    paginator, objects = paginator_from_objects_and_num_and_page(entries, num, page)
    json_source = {'entries': json_source_from_entries(objects),
                   'tag': json_source_from_tags([tag]),
                   'paginator': paginator}

    return json_response(simplejson.dumps(json_source))


def feeds_latest_redirect(request):
    return redirect('http://feeds.feedburner.com/reiare/cPIq', permanent=True)


# mobile's views

def mobile_index(request, page=1):
    entries = Entry.published_objects.all()
    dic, objects = paginator_from_objects_and_num_and_page(entries, 10, page)
    tags = EntryTag.objects.all()
    return render_to_response('2.0/mobile/mobile_index.html',
                              {'object_list': objects,
                               'tag_list': tags,
                               'paginator': dic},
                              context_instance=RequestContext(request))


def mobile_detail(request, year, month, day, slug):
    try:
        entries = Entry.published_objects.filter(created__year=year). \
            filter(created__month=month).filter(created__day=day). \
            filter(**{'slug': slug})
    except:
        raise Http404
    return render_to_response('2.0/mobile/mobile_detail.html',
                              {'object': entries[0],
                              'has_home_button': True,},
                              context_instance=RequestContext(request))


def mobile_tag_index(request):
    return render_to_response('2.0/mobile/mobile_tags.html',
                              {'tags': EntryTag.objects.all(),
                               'has_home_button': True,},
                              context_instance=RequestContext(request))

def mobile_archive_index(request):
    pass


def mobile_tag(request):
    pass


def mobile_month(request):
    pass

