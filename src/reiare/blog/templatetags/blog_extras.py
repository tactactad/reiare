# -*- coding: utf-8 -*-
import random, urllib, re, datetime
from xml.etree import ElementTree

from django import template
from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.core.cache import cache
from django.utils.encoding import force_unicode

from blog.models import Entry, EntryTag, EntryArchive, AmazonAsamashi, Comment
from blog import lastfmaccess

register = template.Library()

@register.filter(name='omit')
def omit(value, length=15):
    #s = unicode(value, 'utf-8', 'replace')
    #s = force_unicode(value, encoding='utf-8', errors='replace')
    s = value
    if length < 10:
        length = 10

    if len(s) > length:
        back_length = length // 3
        temp = s[:length-back_length]
        temp += u"…" + s[len(s)-(back_length-1):]

        s = temp
    return s

@register.filter(name='convert_unicode')
def convert_unicode(value):
    #return unicode(value, 'utf-8')
    #return smart_unicode(value, encoding='utf-8')
    return value

@register.filter(name='img_simpleapi')
def img_simpleapi(value):
    tag_re = re.compile(r'<isa src="http://.">')
    return value

@register.filter(name='add_target_self')
def add_target_self(value):
    #tag_re = re.compile(r'<a href=')
    #return tag_re.sub('<a target="_self" href=', value)
    return value.replace('<a href=', '<a target="_self" href=')

@register.inclusion_tag('archive_list.html')
def show_archives(month=None):
    archives = EntryArchive.objects.all()
    if month:
            return {'archives': archives, 'year': month.strftime("%Y"), 'month': month.strftime("%m")}
    else:
            return {'archives':archives, 'year': "0000", 'month': "00"}

@register.inclusion_tag('tag_list.html')
def show_tags():
    tags = EntryTag.objects.all()
    return {'tags': tags}

@register.inclusion_tag('recent_entries.html')
def show_recent_entries(num=10, page=1):
    start_num = (page - 1) * num
    end_num = start_num + num
    entries = Entry.published_objects.filter(created__lte=datetime.datetime.now())[start_num:end_num]
    return {'entries': entries,
            'previous': page-1}

@register.inclusion_tag('random_entries.html')
def show_random_entries(num=10):
    if cache.get('random_entries'):
        entries = cache.get('random_entries')
    else:
        if num > Entry.published_objects.count():
            num = Entry.published_objects.count()

        latest_entry = Entry.published_objects.order_by('-id')[:1].get()
        entries = set()
        while len(entries) < num:
            id = random.randint(1, latest_entry.id)
            try:
                entry = Entry.published_objects.get(id__exact=id, created__lte=datetime.datetime.now())
                entries.add(entry)
            except:
                pass
        cache.set('random_entries', entries, 86400)
    return {'entries': entries}

@register.inclusion_tag('recent_comments.html')
def show_recent_comments(num=10, page=1):
    start_num = (page -1) * num
    end_num = start_num + num
    comments = Comment.published_objects.all()[start_num:end_num]
    return {'comments': comments, 'previous': page-1}

@register.inclusion_tag('asamashies.html')
def show_asamashies(show_asamashies='True', show_spot_asamashi='False'):
    if bool(show_asamashies):
        if cache.get('asamashies_items'):
            items = cache.get('asamashies_items')
        else:
            asamashies = AmazonAsamashi.published_objects.all()
            asins = []
            for asamashi in asamashies:
                asins.append(asamashi.asin)

            asins = ','.join(asins)
            try:
                #print "http://webservices.amazon.co.jp/onca/xml?Service=AWSECommerceService&AWSAccessKeyId=" + settings.AWS_ACCESS_KEY_ID + "&AssociateTag=" + settings.AWS_ASSOCIATE_TAG + "&Operation=ItemLookup&ItemId=" + asins + "&ResponseGroup=Medium,OfferListings&Version=2007-02-22"
                results = ElementTree.parse(urllib.urlopen("http://webservices.amazon.co.jp/onca/xml?Service=AWSECommerceService&AWSAccessKeyId=" + settings.AWS_ACCESS_KEY_ID + "&AssociateTag=" + settings.AWS_ASSOCIATE_TAG + "&Operation=ItemLookup&ItemId=" + asins + "&ResponseGroup=Medium,OfferListings&Version=2007-02-22"))
                url = '{http://webservices.amazon.com/AWSECommerceService/2007-02-22}'

                items = []
                for result in results.findall('%sItems/%sItem' % (url, url)):
                    try:
                        asin = result.find('%sASIN' % (url)).text
                        asamashi = asamashies.get(asin=asin)
                        try:
                            small_image_url = result.find('%sSmallImage/%sURL' % (url, url)).text
                        except:
                            small_image_url = "http://rcm-images.amazon.com/images/G/09/x-locale/detail/thumb-no-image._SL100_SCTZZZZZZZ_.jpg"

                        try:
                            point = result.find('%sOffers/%sOffer/%sLoyaltyPoints/%sPoints' % (url, url, url, url)).text
                        except:
                            point = None

                        item = {'comment': asamashi.comment,
                                'priority': asamashi.priority,
                                'created': asamashi.created,
                                'imgsrc': small_image_url,
                                'url': result.find('%sDetailPageURL' % (url)).text,
                                'title': result.find('%sItemAttributes/%sTitle' % (url, url)).text,
                                'price': result.find('%sOffers/%sOffer/%sOfferListing/%sPrice/%sFormattedPrice' % (url, url, url, url, url)).text,
                                #'price': result.find('%sOfferSummary/%sLowestRefurbishedPrice/%sFormattedPrice' % \
                                 #   (url, url, url)).text,
                                'point': point}
                        items.append(item)
                    except:
                        pass

            except:
                items = None
            cache.set('asamashies_items', items, 21600)

	return {'asamashies': items,
		'SHOW_ASAMASHIES': 'True',
		'SHOW_SPOT_ASAMASHI': show_spot_asamashi}

    else:
        return {'asamashies': None,
		'SHOW_ASAMASHIES': 'False',
		'SHOW_SPOT_ASAMASHI': show_spot_asamashi}

def cmp_asamashi(a, b):
    if cmp(b['priority'], a['priority']) == 0:
        return cmp(b['created'], a['created'])
    return cmp(b['priority'], a['priority'])

@register.inclusion_tag('amazon_asamashi.html')
def show_amazon_asamashi(asin):
    try:
        url = '{http://webservices.amazon.com/AWSECommerceService/2006-11-14}'
        xml = ElementTree.parse(urllib.urlopen("http://webservices.amazon.co.jp/onca/xml?Service=AWSECommerceService&AWSAccessKeyId=" + settings.AWS_ACCESS_KEY_ID + "&AssociateTag=" + settings.AWS_ASSOCIATE_TAG + "&Operation=ItemLookup&ItemId=" + asin + "&ResponseGroup=Medium&Version=2006-11-14"))

        try:
            smallImageURL = xml.find(url + 'Items/' + url + 'Item/' + url + 'SmallImage/' + url + 'URL').text

	except:
            smallImageURL = "http://rcm-images.amazon.com/images/G/09/x-locale/detail/thumb-no-image._SL100_SCTZZZZZZZ_.jpg"

        item = {'url': xml.find(url + 'Items/' + url + 'Item/' + url + 'DetailPageURL').text,
                'imgsrc': smallImageURL,
                'title': xml.find(url + 'Items/' + url + 'Item/' + url + 'ItemAttributes/' + url + 'Title').text,
                'price': xml.find(url + 'Items/' + url + 'Item/' + url + 'OfferSummary/' + url + 'LowestNewPrice/' + url + 'FormattedPrice').text}

    except:
        item = None

    return {'item': item}

class IncludeHTMLNode(template.Node):
    def __init__(self, url):
        self.url = url

    def render(self, context):
        return urllib.urlopen(self.url).read()

@register.tag(name="include_html")
def do_include_html(parser, token):
    try:
        tag_name, url = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single #argument." % token.contents[0]

    if not (url[0] == url[-1] and url[0] in ('"', "'")):
        raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name

    return IncludeHTMLNode(url[1:-1])

@register.filter(name='list_table_tr')
def list_table_tr(value, num="5"):
    if (value % int(num)) == 0:
        return "</tr><tr>"

    return ""

@register.filter(name='flat_page_content_by_url')
def flat_page_content_by_url(value):
    try:
        flat_page = FlatPage.objects.get(url=value)
	content = flat_page.content
    except:
        content = ""

    return content

def paginator(context, adjacent_pages=2):
    """
    To be used in conjunction with the object_list generic view.

    Adds pagination context variables for use in displaying first, adjacent and
    last page links in addition to those created by the object_list generic
    view.
    """
    page_numbers = [n for n in \
                    range(context["page"] - adjacent_pages, context["page"] + adjacent_pages + 1) \
                    if n > 0 and n <= context["pages"]]
    return {
        "hits": context["hits"],
        "results_per_page": context["results_per_page"],
        "page": context["page"],
        "pages": context["pages"],
        "page_numbers": page_numbers,
        "next": context["next"],
        "previous": context["previous"],
        "has_next": context["has_next"],
        "has_previous": context["has_previous"],
        "show_first": 1 not in page_numbers,
        "show_last": context["pages"] not in page_numbers,
    }

register.inclusion_tag("paginator.html", takes_context=True)(paginator)

@register.inclusion_tag('lastfm.html')
def show_lastfm_recent_tracks(user, mode):
    from blog.views import get_lastfm_user_profile_items
    if mode == 'recent_tracks':
        items = get_lastfm_user_profile_items('RECENT_TRACKS', 'lastfm_recent_tracks', 600)
        template_name = 'lastfm_recent_tracks.html'
    elif mode == 'recent_weekly_track_chart':
        items = get_lastfm_user_profile_items('RECENT_WEEKLY_TRACK_CHART', 'lastfm_recent_weekly_track_chart')
        template_name = 'lastfm_recent_weekly_track_chart.html'
    elif mode == 'recent_weekly_artist_chart':
        items = get_lastfm_user_profile_items('RECENT_WEEKLY_ARTIST_CHART', 'lastfm_recent_weekly_artist_chart')
        template_name = 'lastfm_recent_weekly_artist_chart.html'
    elif mode == 'top_artists':
        items = get_lastfm_user_profile_items('TOP_ARTISTS', 'lastfm_top_artists')
        template_name = 'lastfm_top_artists.html'
    elif mode == 'top_tracks':
        items = get_lastfm_user_profile_items('TOP_TRACKS', 'lastfm_top_tracks')
        template_name = 'lastfm_top_tracks.html'
    else:
        items = get_lastfm_user_profile_items('RECENT_TRACKS', 'lastfm_recent_tracks', 600)
        template_name = 'lastfm_recent_tracks.html'

    return {'objects': items,
            'lastfm_id': user,
            'template_name': template_name}
