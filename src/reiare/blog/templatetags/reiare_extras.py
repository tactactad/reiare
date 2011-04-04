# -*- coding: utf-8 -*-
import re

from django import template
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter(name='remove_linebreaks')
@stringfilter
def remove_linebreaks_using_regex(value, regex):
    for mo in re.finditer(regex, value, re.S):
        tmp = mo.group().replace('<br />', '\n')
        tmp = tmp.replace('<p>', '')
        tmp = tmp.replace('</p>', '')
        value = value.replace(mo.group(), tmp)
    return value


@register.filter(name='omit')
@stringfilter
def omit(value, length=15):
    s = value
    if length < 10:
        length = 10

    if len(s) > length:
        back_length = length // 3
        temp = s[:length-back_length]
        temp += u"…" + s[len(s)-(back_length-1):]

        s = temp
    return s


@register.filter(name='wrapped_jQuery_templatetag')
@stringfilter
def wrapped_jQuery_templatetag(value):
    return '{{' + value + '}}'


@register.filter(name='rewrite_img_src')
@stringfilter
def rewrite_img_src(value):
    for mo in re.finditer('<img src="/site_media/', value, re.S):
        tmp = mo.group().replace('/site_media/', 'http://reiare.net/site_media/')
        value = value.replace(mo.group(), tmp)
    return value


@register.filter(name='rewrite_a_href')
@stringfilter
def rewrite_a_href(value):
    for mo in re.finditer('<a href="/blog/', value, re.S):
        tmp = mo.group().replace('/blog/', 'http://reiare.net/blog/')
        value = value.replace(mo.group(), tmp)
    return value
