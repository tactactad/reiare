# -*- coding: utf-8 -*-
import datetime, time, urllib, re
from xml.etree import ElementTree
import re

from django.views.generic.list_detail import object_list
from django.views.generic.date_based import object_detail
from django.contrib.syndication.views import feed
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext
from django.conf import settings
from django.db.models.query import Q
#from django.views.decorators.cache import cache_page
from django.core.cache import cache

from django.utils.encoding import smart_str, smart_unicode

from blog.models import Entry, Comment, EntryTag, EntryImage
from blog.urls import feeds, info_dict
#from mail import send_mail
from django.core.mail import send_mail
from blog.forms import CommentForm, SearchForm
from blog import lastfmaccess

def tag_list(request, tag, page=None):
    if request.GET.has_key('mode'):
        mode = request.GET['mode']
    else:
        mode = None

    if request.COOKIES.has_key('entry_list_mode'):
        list_mode = request.COOKIES['entry_list_mode']

        if mode == "open":
            list_mode = "open"
        elif mode == "close":
            list_mode = "close"

        if not (list_mode == "open" or list_mode == "close"):
            list_mode = "open"
    else:
        list_mode = "open"

    try:
        tag = EntryTag.objects.get(name__iexact=tag)
    except:
        raise Http404

    page =  object_list(request,
        Entry.published_objects.filter(tags__name__iexact=tag).filter(created__lte=datetime.datetime.now()).select_related(),
        paginate_by=settings.PAGINATE_NUM,
        extra_context={ 'tag': tag, 'list_mode': list_mode }, allow_empty=True, page=page)
    page.set_cookie('entry_list_mode', list_mode, expires=cookie_expires_value(), path='/', domain=None, secure=None)
    return page

def cookie_expires_value():
    today = datetime.datetime.now()
    td = datetime.timedelta(days=30, seconds=-3600*9)
    return (today + td).strftime('%a, %d %b %Y %H:%M:%S GMT')
    #return (mx.DateTime.now() + mx.DateTime.RelativeDateTime(months=+1, hours=-9)).strftime('%a, %d %b %Y %H:%M:%S GMT')

def tag_image_list(request, tag, page=None):
    try:
        tag = EntryTag.objects.get(name__iexact=tag)
        entry_images = EntryImage.objects.filter(tags__name__iexact=tag.name).filter(is_publish=True)
        print len(entry_images)
    except:
        raise Http404

    return object_list(request, entry_images, paginate_by=settings.PAGINATE_NUM,
        extra_context={'tag': tag}, page=page)

def comment_form(request):
    if request.COOKIES.has_key('commentName'):
        form = CommentForm(initial={'author': request.COOKIES['commentName']})
    else:
        form = CommentForm()

    return form

def detail(request, year, month, day, slug):
    form = comment_form(request)

    _dict = dict(info_dict, slug=slug, month_format='%m', slug_field='slug',
        extra_context = {
            'do_display_comments': True,
            'do_display_comment_form': True,
            'form': form,
        })
    return object_detail(request, year, month, day, **_dict)

def get_entry(year, month, day, slug):
    try:
        date = datetime.date(*time.strptime(year+month+day, '%Y%m%d')[:3])
    except ValueError:
        raise Http404

    entries = Entry.published_objects.filter(slug__exact=slug,
        created__range=(datetime.datetime.combine(date, datetime.time.min),
        datetime.datetime.combine(date, datetime.time.max)))

    if len(entries) == 0:
        raise Http404

    return entries[0]

def post_comment(request, year, month, day, slug):
    try:
        entry = get_entry(year, month, day, slug)
    except:
        raise Http404

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            r = re.compile('(\w+\s+\n)|[<>"=]', re.I)
            #r = re.compile('<a href=', re.I)
            if not r.search(form.cleaned_data['body']) == None:
                return HttpResponseForbidden('<h1>403 Forbidden.</h1>')

            add_comment(form, entry)

            page = HttpResponseRedirect(entry.get_absolute_url())
            page.set_cookie('commentName', form.cleaned_data['author'].encode('utf-8'), expires=cookie_expires_value(), path='/', domain=None, secure=None)
            return page

        else:
            form = CommentForm()

        return render_to_response('blog/entry_detail.html',
            dict(form=form, object=entry, do_display_comments=True,
                do_display_comment_form=True),
            context_instance=RequestContext(request))
    return HttpResponseForbidden('<h1>403 Forbidden.</h1>')

def add_comment(form, entry):
    comment = Comment(author = form.cleaned_data['author'],
        body = form.cleaned_data['body'],
        entry = entry,
        is_publish = True)
    comment.save()

    send_comment_mail(comment)

def send_comment_mail(comment):
    body = settings.BLOG_TITLE + "さんにこめんとがあったりしました。\n\n"
    body += "おなまえ: " + comment.author.encode('utf-8') + "\n"
    body += "ないよう:\n" + comment.body.encode('utf-8') + "\n\n"
    body += settings.BLOG_HOST_URL + comment.entry.get_absolute_url()
    send_mail(settings.BLOG_TITLE + ' こめんと', body + "\n", settings.DEFAULT_FROM_EMAIL, [settings.BLOG_MASTER_EMAIL])
    #send_mail('subject', 'body', 'tac@reiare.net', ['tactactad@gmail.com'])

def no_cache_page(page):
    page['Pragma'] = 'no-cache'
    page['Cache-Control'] = 'no-cache'
    page['Expires'] = 'Thu, 30 Nov 1972 17:00:00 GMT'
    return page

def get_comment(request, object_id):
    try:
        entry = Entry.published_objects.get(pk=object_id)
    except:
        raise Http404

    form = comment_form(request)

    page = render_to_response('entry_comment.html', {'entry': entry, 'form': form})
    return no_cache_page(page)

def post_comment_ajax(request, object_id):
    try:
        entry = Entry.published_objects.get(pk=object_id)
    except:
        raise Http404

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            r = re.compile('(\w+\s+\n)|[<>"=]', re.I)
            #r = re.compile('[\w\s\n]?', re.I)
            #r = re.compile('<a href=', re.I)
            if not r.search(form.cleaned_data['body']) == None:
                raise Http404

            add_comment(form, entry)

            page = HttpResponseRedirect('/blog/comment/' + object_id + '/')
            page.set_cookie('commentName', form.cleaned_data['author'].encode('utf-8'), expires=cookie_expires_value(), path='/', domain=None, secure=None)
            return no_cache_page(page)
        else:
            form = CommentForm()

        page = render_to_response('entry_comment.html', {'comments': entry.published_comment_list(), 'entry': entry, 'form': form})
        return no_cache_page(page)

def asin2asamashi(request, associate_tag, asins):
    import hashlib, hmac
    import base64

    timestamp = datetime.datetime.utcnow().isoformat()

    parameters = 'AWSAccessKeyId=' + settings.AWS_ACCESS_KEY_ID + \
        '&AssociateTag=' +  urllib.quote(associate_tag) + \
        '&ItemId=' + urllib.quote(asins) + \
        '&Operation=ItemLookup' + \
        '&RsesponseGroup=Small' + \
        '&Service=AWSECommerceService' + \
        '&Timestamp=' + urllib.quote(timestamp) + \
        '&Version=' + urllib.quote(settings.AWS_VERSION)

    signature = '\n'.join(['GET', settings.AWS_HOSTNAME, '/onca/xml', parameters])
    signature = hmac.new(settings.AWS_SECRET_ACCESS_KEY, signature, hashlib.sha256).digest()
    signature = urllib.quote(base64.b64encode(signature))

    request_uri = 'http://' + settings.AWS_HOSTNAME + '/onca/xml?' + parameters + '&Signature=' + signature
    try:
        url = '{http://webservices.amazon.com/AWSECommerceService/' + settings.AWS_VERSION + '}'
        results = ElementTree.parse(urllib.urlopen(request_uri))
        items = []
        for result in results.findall('%sItems/%sItem' % (url, url)):
            item = {
                'url': result.find('%sDetailPageURL' % (url)).text,
                'title': result.find('%sItemAttributes/%sTitle' % (url, url)).text
            }
            items.append(item)
    except:
        items = None

    return render_to_response('asin2asamashi.html', {'items': items})

def get_body(request, object_id):
    try:
        entry = Entry.published_objects.get(pk=object_id)
    except:
        raise Http404

    form = comment_form(request)

    return render_to_response('entry_body.html', {'entry': entry, 'form': form})

def get_blog_preview(request):
    perms = ['blog.add_entry', 'blog.change_entry']
    if not request.user.has_perms(perms):
        raise Http404

    if request.method == "POST":
        preview_data = request.POST.copy()
        entry = Entry(title=preview_data['title'], body=preview_data['body'], created=datetime.datetime.now())
    else:
        entry = None

    return render_to_response('blog/entry_detail.html', dict(object = entry, PREVIEW = True),
        context_instance=RequestContext(request))

def get_search_result(request):
    if request.method == "POST":
        search_form = SearchForm(request.POST)

        querys = []
        for keyword in re.split(' |　', search_form.data['keyword']):
            q = Q(title__contains=keyword)|Q(body__contains=keyword)
            querys.append(q)
        results = Entry.published_objects.filter(*querys)
    else :
        search_form = SearchForm()
        results = None

    return render_to_response('search_result.html',
                              {'search_form': search_form,
                               'results': results},
                              context_instance=RequestContext(request))

#def no_cached_page(func):
#    page = no_cache_page(func)
#    return page

def get_lastfm_user_profile_items(operation, cache_name, expires=86400, slice=10):
    if cache.get(cache_name):
        return cache.get(cache_name)
    else:
        res = lastfmaccess.get_response('USER_PROFILE', settings.LASTFM_ID, operation)
        cache.set(cache_name, res.items[:slice], expires)
        return res.items[:slice]

def get_lastfm_recent_tracks(request):
    items = get_lastfm_user_profile_items('RECENT_TRACKS', 'lastfm_recent_tracks', 600)
    page = render_to_response('lastfm_recent_tracks.html',
                              {'objects': items, 'lastfm_id': settings.LASTFM_ID})
    page.set_cookie('lastfm_mode', 'recent_tracks', expires=cookie_expires_value(), path='/', domain=None, secure=None)
    return no_cache_page(page)

def get_lastfm_recent_weekly_track_chart(request):
    items = get_lastfm_user_profile_items('RECENT_WEEKLY_TRACK_CHART', 'lastfm_recent_weekly_track_chart')
    page = render_to_response('lastfm_recent_weekly_track_chart.html',
                              {'objects': items, 'lastfm_id': settings.LASTFM_ID})
    page.set_cookie('lastfm_mode', 'recent_weekly_track_chart', expires=cookie_expires_value(), path='/', domain=None, secure=None)
    return no_cache_page(page)

def get_lastfm_recent_weekly_artist_chart(request):
    items = get_lastfm_user_profile_items('RECENT_WEEKLY_ARTIST_CHART', 'lastfm_recent_weekly_artist_chart')
    page = render_to_response('lastfm_recent_weekly_artist_chart.html',
                              {'objects': items, 'lastfm_id': settings.LASTFM_ID})
    page.set_cookie('lastfm_mode', 'recent_weekly_artist_chart', expires=cookie_expires_value(), path='/', domain=None, secure=None)
    return no_cache_page(page);

def get_lastfm_top_artists(request):
    items = get_lastfm_user_profile_items('TOP_ARTISTS', 'lastfm_top_artists')
    page = render_to_response('lastfm_top_artists.html',
                              {'objects': items, 'lastfm_id': settings.LASTFM_ID})
    page.set_cookie('lastfm_mode', 'top_artists', expires=cookie_expires_value(), path='/', domain=None, secure=None)
    return no_cache_page(page)

def get_lastfm_top_tracks(request):
    items = get_lastfm_user_profile_items('TOP_TRACKS', 'lastfm_top_tracks')
    page = render_to_response('lastfm_top_tracks.html',
                              {'objects': items, 'lastfm_id': settings.LASTFM_ID})
    page.set_cookie('lastfm_mode', 'top_tracks', expires=cookie_expires_value(), path='/', domain=None, secure=None)
    return no_cache_page(page)

def get_recent_entries(request, page_num='1'):
    start_num = (int(page_num) - 1) * settings.SIDEBAR_ENTRIES_NUM
    end_num = start_num + settings.SIDEBAR_ENTRIES_NUM
    entries = Entry.published_objects.filter(created__lte=datetime.datetime.now())[start_num:end_num]
    page = render_to_response('recent_entries_box.html',
                              {'entries': entries, 'previous': int(page_num)-1})
    page.set_cookie('recent_entries_page', page_num)
    return no_cache_page(page)

def get_recent_comments(request, page_num='1'):
    start_num = (int(page_num) -1) * settings.SIDEBAR_ENTRIES_NUM
    end_num = start_num + settings.SIDEBAR_ENTRIES_NUM
    comments = Comment.published_objects.all()[start_num:end_num]
    page = render_to_response('recent_comments_box.html',
                              {'comments': comments, 'previous': int(page_num)-1})
    page.set_cookie('recent_comments_page', page_num)
    return no_cache_page(page)

def get_more_entries(request, page_num='2'):
    start_num = (int(page_num)-1) * 5
    end_num = start_num + 5
    entries = Entry.published_objects.all()[start_num:end_num]

    return render_to_response('more_entries.html',
                              {'entries': entries,
                               'is_ajax': True})

def get_iui_page(request):
    recent_entries = Entry.published_objects.all()[:10]
    tags = EntryTag.objects.all()

    return render_to_response('iui_base.html',
                              {'recent_entries': recent_entries,
                               'tags': tags,
                               'form': comment_form(request)})

def get_iui_more_entries(request, page_num='2'):
    start_num = (int(page_num)-1) * 10
    end_num = start_num + 10
    entries = Entry.published_objects.all()[start_num:end_num]

    return render_to_response('iui_more_entries.html',
                              {'entries': entries,
                               'page_num': int(page_num)+1})

def get_iui_entry(request, year, month, day, slug):
    try:
        entry = get_entry(year, month, day, slug)
    except:
        raise Http404

    return render_to_response('iui_entry.html',
                              {'entry': entry,
                               'form': comment_form(request)})

def get_iui_entries_by_tag(request, tag):
    entries = Entry.published_objects.filter(tags__name__iexact=tag).filter(created__lte=datetime.datetime.now())[:10]

    return render_to_response('iui_entries_by_tag.html',
                              {'tag': tag,
                               'entries': entries})

def get_iui_more_entries_by_tag(request, tag, page_num='2'):
    start_num = (int(page_num)-1) * 10
    end_num = start_num + 10
    entries = Entry.published_objects.filter(tags__name__iexact=tag).filter(created__lte=datetime.datetime.now())[start_num:end_num]

    return render_to_response('iui_more_entries.html',
                              {'entries': entries,
                               'tag': tag,
                               'page_num': int(page_num)+1})

def post_iui_entry_comment(request, object_id):
    try:
        entry = Entry.published_objects.get(pk=object_id)
    except:
        raise Http404

    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            r = re.compile('(\w+\s+\n)|[<>"=]', re.I)
            if not r.search(form.clean_data['body']) == None:
                raise Http404

            add_comment(form, entry)

            page = render_to_response('iui_entry_comment_box.html',
                                      {'entry': entry,
                                       'form': comment_form(request)})
            page.set_cookie('commentName', form.clean_data['author'], expires=cookie_expires_value(), path='/', domain=None, secure=None)
            return no_cache_page(page)

        page = render_to_response('iui_entry_comment_box.html', {'comments': entry.published_comment_list(), 'entry': entry, 'form': comment_form(request)})
        return no_cache_page(page)
