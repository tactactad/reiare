# -*- coding: utf-8 -*-
from django.conf import settings

def blog_context(request):
    if request.COOKIES.has_key('lastfm_mode'):
        lastfm_mode = request.COOKIES['lastfm_mode']
    else:
        lastfm_mode = 'recent_tracks'

    if request.COOKIES.has_key('recent_entries_page'):
        try:
            recent_entries_page = int(request.COOKIES['recent_entries_page'])
        except:
            recent_entries_page = 1
    else:
        recent_entries_page = 1

    if request.COOKIES.has_key('recent_comments_page'):
        try:
            recent_comments_page = int(request.COOKIES['recent_comments_page'])
        except:
            recent_comments_page = 1
    else:
        recent_comments_page = 1

    return {
        'BLOG_TITLE': settings.BLOG_TITLE,
	'BLOG_SUB_TITLE': settings.BLOG_SUB_TITLE,
	'SHOW_BANNERS': settings.SHOW_BANNERS,
        'SHOW_TOP_SIDEBAR': settings.SHOW_TOP_SIDEBAR,
        'SHOW_ASAMASHIES': settings.SHOW_ASAMASHIES,
        'SHOW_GOOGLE_SEARCH': settings.SHOW_GOOGLE_SEARCH,
        'SHOW_TOPIC': settings.SHOW_TOPIC,
        'SHOW_SPOT_ASAMASHI': settings.SHOW_SPOT_ASAMASHI,
        'SHOW_PROFILE': settings.SHOW_PROFILE,
        'SHOW_ASAMASHISITE_LINKS': settings.SHOW_ASAMASHISITE_LINKS,
        'LASTFM_ID': settings.LASTFM_ID,
        'LASTFM_MODE': lastfm_mode,
        'RECENT_ENTRIES_PAGE': recent_entries_page,
        'SIDEBAR_ENTRIES_NUM': settings.SIDEBAR_ENTRIES_NUM,
        'RECENT_COMMENTS_PAGE': recent_comments_page
    }
