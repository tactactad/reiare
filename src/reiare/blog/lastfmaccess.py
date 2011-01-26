# -*- coding: utf-8 -*-
import urllib, socket
from xml.etree import ElementTree

BASE_REQUEST_URL = 'http://ws.audioscrobbler.com'
VERSION = '1.0'

CATEGORY = {
    'USER_PROFILE': 'user',
    'ARTIST': 'artist',
    'ALBUM': 'album',
    'TRACK': 'track',
    'TAG': 'tag',
    'GROUP': 'group'
}

USER_PROFILE_OPERATION = {
    'PROFILE_INFORMATION': 'profile.xml',
    'TOP_ARTISTS': 'topartists.xml',
    'TOP_ALBUMS': 'topalbums.xml',
    'TOP_TRACKS': 'toptracks.xml',
    'TOP_TAGS': 'tags.xml',
    'TOP_TAGS_FOR_ARTIST': 'artisttags.xml',
    'TOP_TAGS_FOR_ALBUM': 'albumtags.xml',
    'TOP_TAGS_FOR_TRACK': 'tracktags.xml',
    'FRIENDS_LIST': 'friends.xml',
    'NEIGHBOURS': 'neighbours.xml',
    'RECENT_TRACKS': 'recenttracks.xml',
    'RECENT_BANNED_TRACKS': 'recentbannedtracks.xml',
    'RECENT_LOVED_TRACKS': 'recentlovedtracks.xml',
    'WEEKLY_CHART_LIST': 'weeklychartlist.xml',
    'RECENT_WEEKLY_ARTIST_CHART': 'weeklyartistchart.xml',
    'RECENT_WEEKLY_ALBUM_CHART': 'weeklyalbumchart.xml',
    'RECENT_WEEKLY_TRACK_CHART': 'weeklytrackchart.xml',
    'PREVIOUS_WEEKLY_ARTIST_CHART': 'weeklyartistchart.xml',
    'PREVIOUS_WEEKLY_ALBUM_CHART': 'weeklyalbumchart.xml',
    'PREVIOUS_WEEKLY_TRACK_CHART': 'weeklytrackchart.xml',
    'SYSTEM_RECOMMENDATIONS': 'systemrecs.xml',
    'TASTE-O-METER': 'tasteometer.xml'
}

XML_ATTR = {
    'ARTIST': 'artist',
    'NAME': 'name',
    'MBID': 'mbid',
    'ALBUM': 'album',
    'URL': 'url',
    'DATE': 'date',
    'CHART_POSITION': 'chartposition',
    'PLAY_COUNT': 'playcount',
    'RANK': 'rank',
    'THUMBNAIL': 'thumbnail',
    'IMAGE': 'image',
}

ELEMENT_NAME = {
    'RECENT_TRACKS': 'recenttracks',
    'RECENT_WEEKLY_TRACK_CHART': 'weeklytrackchart',
    'RECENT_WEEKLY_ARTIST_CHART': 'weeklyartistchart',
    'TOP_ARTISTS': 'topartists',
    'TOP_TRACKS': 'toptracks',
}

def get_response(category, user_id, op):
    req = Request(category, user_id, op)
    return Response(req)

def request_url(path, query=None):
    if query is None:
        return '%s/%s/%s' % (BASE_REQUEST_URL, VERSION, path)

def fetch(request):
    try:
        socket.setdefaulttimeout(10)
        url = request_url(request.get_path())
        return urllib.urlopen(url).read()
    except:
        return None


class Request(object):

    def __init__(self, category, user_id, op, **opts):
        self.category = category
        self.user_id = user_id
        self.op = op
        self.set_attrs(opts)

    def set_attrs(self, adict):
        for k, v in adict.items():
            setattr(self, k, v)

    def get_path(self):
        return '%s/%s/%s' % (CATEGORY[self.category], self.user_id, USER_PROFILE_OPERATION[self.op])


class Response(object):
    items = []

    def __init__(self, request):
        self.request = request
        self.xml = fetch(request)
        if self.xml: self.parse()

    def parse(self):
        self.items = []
        try:
            et = ElementTree.fromstring(self.xml)
            if et.tag == ELEMENT_NAME['RECENT_TRACKS']:
                for el in et.getchildren():
                    try:
                        item = {'artist': el.find(XML_ATTR['ARTIST']).text,
                                'name': el.find(XML_ATTR['NAME']).text,
                                'mbid': el.find(XML_ATTR['MBID']).text,
                                'album': el.find(XML_ATTR['ALBUM']).text,
                                'url': el.find(XML_ATTR['URL']).text,
                                'date': el.find(XML_ATTR['DATE']).text}
                        self.items.append(item)
                    except:
                        pass

            elif et.tag == ELEMENT_NAME['RECENT_WEEKLY_TRACK_CHART']:
                for el in et.getchildren():
                    try:
                        item = {'artist': el.find(XML_ATTR['ARTIST']).text,
                                'name': el.find(XML_ATTR['NAME']).text,
                                'mbid': el.find(XML_ATTR['MBID']).text,
                                'chart_position': el.find(XML_ATTR['CHART_POSITION']).text,
                                'play_count': el.find(XML_ATTR['PLAY_COUNT']).text,
                                'url': el.find(XML_ATTR['URL']).text}
                        self.items.append(item)
                    except:
                        pass

            elif et.tag == ELEMENT_NAME['RECENT_WEEKLY_ARTIST_CHART']:
                for el in et.getchildren():
                    try:
                        item = {'name': el.find(XML_ATTR['NAME']).text,
                                'mbid': el.find(XML_ATTR['MBID']).text,
                                'chart_position': el.find(XML_ATTR['CHART_POSITION']).text,
                                'play_count': el.find(XML_ATTR['PLAY_COUNT']).text,
                                'url': el.find(XML_ATTR['URL']).text}
                        self.items.append(item)
                    except:
                        pass

            elif et.tag == ELEMENT_NAME['TOP_ARTISTS']:
                for el in et.getchildren():
                    try:
                        item = {'name': el.find(XML_ATTR['NAME']).text,
                                'mbid': el.find(XML_ATTR['MBID']).text,
                                'play_count': el.find(XML_ATTR['PLAY_COUNT']).text,
                                'rank': el.find(XML_ATTR['RANK']).text,
                                'url': el.find(XML_ATTR['URL']).text,
                                'thumbnail': el.find(XML_ATTR['THUMBNAIL']).text,
                                'image': el.find(XML_ATTR['IMAGE']).text}
                        self.items.append(item)
                    except:
                        pass

            elif et.tag == ELEMENT_NAME['TOP_TRACKS']:
                for el in et.getchildren():
                    try:
                        item = {'artist': el.find(XML_ATTR['ARTIST']).text,
                                'name': el.find(XML_ATTR['NAME']).text,
                                'mbid': el.find(XML_ATTR['MBID']).text,
                                'play_count': el.find(XML_ATTR['PLAY_COUNT']).text,
                                'rank': el.find(XML_ATTR['RANK']).text,
                                'url': el.find(XML_ATTR['URL']).text}
                        self.items.append(item)
                    except:
                        pass
        except:
            pass

    def user_id(self):
        return self.request.user_id
