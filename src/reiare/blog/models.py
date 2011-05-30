# -*- coding: utf-8 -*-
import datetime
import urllib
import os
import Image
import re
from xml.etree import ElementTree
import logging

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.cache import cache
from django.template import defaultfilters
from django.db.models import permalink
from django.contrib import admin
from django.utils.encoding import smart_unicode

from blog.templatetags import reiare_extras


class EntryArchive(models.Model):
    """
    EntryArchiveのテスト

    >>> object, flag = EntryArchive.objects.get_or_create(yearmonth='201009')
    >>> object
    <EntryArchive: 201009>

    >>> flag
    True

    >>> object.get_absolute_url()
    '/blog/2010/09/'
    """

    yearmonth = models.CharField(max_length=6, blank=False)

    class Meta:
        ordering = ['-yearmonth']

    @permalink
    def get_absolute_url(self):
        return ('django.views.generic.date_based.archive_month', (), {
            'year': self.year,
            'month': self.month})

    def __unicode__(self):
        """
        >>> object = EntryArchive.objects.get(yearmonth='201009')
        >>> object.__unicode__()
        u'201009'
        """
        return self.yearmonth

    def _year(self):
        """
        >>> EntryArchive.objects.get(yearmonth='201009').year
        u'2010'
        """
        return smart_unicode(self.yearmonth[:4])
    year = property(_year)

    def _month(self):
        """
        >>> EntryArchive.objects.get(yearmonth='201009').month
        u'09'
        """
        return self.yearmonth[4:6]
    month = property(_month)

    def verbose_month(self):
        """
        >>> EntryArchive.objects.get(yearmonth='201009').verbose_month()
        u'9'
        >>> object, flag = EntryArchive.objects.get_or_create(yearmonth='201010')
        >>> object.verbose_month()
        '10'
        """
        if self.yearmonth[4:5] == '0':
            return self.yearmonth[5:6]
        else:
            return self.yearmonth[4:6]

    def is_jan(self):
        """
        >>> EntryArchive.objects.get(id=1).is_jan()
        False
        >>> object, flag = EntryArchive.objects.get_or_create(yearmonth='201001')
        >>> object.is_jan()
        True
        """
        return self.month == '01'


class EntryTag(models.Model):
    """
    >>> object, flag = EntryTag.objects.get_or_create(name='test')
    >>> flag
    True
    >>> object.get_absolute_url()
    '/blog/tag/test/'
    >>> object.get_feeds_url()
    '/blog/feeds_ad/tag/test/'
    >>> object.get_touch_url()
    '/blog/touch/tag/test/'
    """
    name = models.CharField('名称', max_length=100, blank=False, unique=True, help_text='重複不可')

    class Meta:
        ordering = ['name']
        verbose_name = 'たぐ'
        verbose_name_plural = 'たぐ'

    def __unicode__(self):
        """
        >>> EntryTag.objects.get(id=1).__unicode__()
        u'test'
        """
        return self.name

    @permalink
    def get_absolute_url(self):
        return ('blog.apis.tag_entries_index', (), {
            'tag': defaultfilters.urlencode(self.name)})

    @permalink
    def get_feeds_url(self):
        return ('blog_feeds', (), {
            'url': 'tag/%s' % defaultfilters.urlencode(self.name)})

    @permalink
    def get_touch_url(self):
        return ('blog.views.get_iui_entries_by_tag', (),
                {'tag': defaultfilters.urlencode(self.name)})


class PublishedEntryManager(models.Manager):
    def get_query_set(self):
        return super(PublishedEntryManager, self).get_query_set().filter(is_publish=True)


class Entry(models.Model):
    """
    >>> user, flag = User.objects.get_or_create(username='testuser')
    >>> object, flag = Entry.objects.get_or_create(title=u'タイトル', body=u'\u3000本文', slug='slug',
    ... created=datetime.datetime(2010, 11, 5, 17, 7, 16), created_by=user, is_publish=True)
    >>> flag
    True
    >>> object.title == unicode(u'タイトル')
    True
    >>> object, flag = Entry.objects.get_or_create(title=u'for mobile img test',
    ... body=u'<img src="/site_media/images/a_medium.jpg" width="500" height="375" /> image',
    ... slug='img', created=datetime.datetime(2011, 5, 30, 11, 32, 22), created_by=user, is_publish=True)
    >>> flag
    True
    >>> object, flag = Entry.objects.get_or_create(title=u'for mobile url test',
    ... body=u'<a href="/blog/spamhamegg/">link</a>',
    ... slug='url', created=datetime.datetime(2011, 5, 30, 11, 33, 22), created_by=user, is_publish=True)
    >>> flag
    True

    >>> object = Entry.published_objects.get(slug='slug')
    >>> object.get_absolute_url()
    '/blog/2010/11/05/slug/'
    >>> object.get_touch_url()
    '/blog/touch/2010/11/05/slug/'
    >>> object.json_url()
    '/blog/api/entry/2.json'
    >>> object.ajax_url()
    u'/blog/#!/blog/2010/11/05/slug/'
    """
    title = models.CharField("タイトル", max_length=200, blank=False)
    body = models.TextField("本文", blank=False)
    slug = models.SlugField("スラグ", unique_for_date='created')
    created = models.DateTimeField("公開日時")
    updated = models.DateTimeField("変更日時", auto_now=True)
    is_publish = models.BooleanField("公開する", blank=False)
    allow_comment = models.BooleanField("コメントを受け付ける", blank=False, default=True)
    comment_count = models.IntegerField("コメント数", default=0, editable=False)

    created_by = models.ForeignKey(User, related_name='entries', verbose_name="投稿者")
    tags = models.ManyToManyField(EntryTag)
    rel_entries = models.ManyToManyField('self', blank=True)

    objects = models.Manager()
    published_objects = PublishedEntryManager()

    class Meta:
        get_latest_by = 'created'
        ordering = ['-created']
        verbose_name_plural = 'えんとりー'
        verbose_name = 'えんとりー'

    def __unicode__(self):
        """
        >>> Entry.published_objects.get(slug='slug').__unicode__() == unicode(u'タイトル')
        True
        """
        return self.title

    def save(self, *args, **kwargs):
        """
        >>> EntryArchive.objects.get(yearmonth='201011')
        <EntryArchive: 201011>
        """
        super(Entry, self).save(*args, **kwargs)
        EntryArchive.objects.get_or_create(yearmonth='%4d%02d' % (self.created.year, self.created.month))

    @permalink
    def get_absolute_url(self):
        return ('blog.apis.detail', (), {'year': self.created.year,
                                          'month': self.created.strftime('%m'),
                                          'day': self.created.strftime('%d'),
                                          'slug': self.slug})

    @permalink
    def get_touch_url(self):
        return ('blog.views.get_iui_entry', (), {'year': self.created.year,
                                                 'month': self.created.strftime('%m'),
                                                 'day': self.created.strftime('%d'),
                                                 'slug': self.slug})

    @permalink
    def json_url(self):
        return('blog.apis.entry_json', (), {
                'object_id': self.id
                })

    def ajax_url(self):
        return '/blog/#!/blog/%s/%s/%s/%s/' % (self.created.year,
                                               self.created.strftime('%m'),
                                               self.created.strftime('%d'),
                                               self.slug)

    @permalink
    def mobile_url(self):
        return('blog.apis.mobile_detail',(), {'year': self.created.year,
                                              'month' : self.created.strftime('%m'),
                                              'day': self.created.strftime('%d'),
                                              'slug': self.slug})


    def published_comment_list(self):
        return self.comments.filter(is_publish=True).order_by('created')

    def published_comment_count(self):
        if self.comments.filter(is_publish=False):
            return self.comment_count - self.comments.filter(is_publish=False).count()
        else:
            return self.comment_count

    def published_rel_entries(self):
        return self.rel_entries.filter(is_publish=True)

    def now_datetime(self):
        return datetime.datetime.now()

    def self_id(self):
        """
        >>> Entry.published_objects.get(slug='slug').self_id()
        2
        """
        return self.id

    def attr_created(self):
        """
        >>> Entry.published_objects.get(slug='slug').attr_created()
        u'2010-11-05T17:07:16+0900'
        """
        return defaultfilters.date(self.created, "Y-m-d\TH:i:sO")

    def display_created(self):
        """
        >>> Entry.published_objects.get(slug='slug').display_created()
        u'2010/11/5 (Fri) p.m.05:07'
        """
        return defaultfilters.date(self.created, "Y/n/j (D) ah:i")

    def linebreaks_body(self):
        """
        >>> Entry.published_objects.get(slug='slug').linebreaks_body() == unicode(u'<p>本文</p>')
        True
        """
        return defaultfilters.linebreaks(self.remove_indent_body())

    def linebreaks_body_without_pre(self):
        """
        >>> Entry.published_objects.get(slug='slug').linebreaks_body_without_pre() == unicode(u'<p>本文</p>')
        True
        """
        return reiare_extras.remove_linebreaks_using_regex(self.linebreaks_body(),
                                                           '<pre.*?</pre>')

    def linebreaks_body_for_mobile(self):
        """
        >>> Entry.published_objects.get(slug='img').linebreaks_body_for_mobile()
        u'<p><img src="/site_media/images/a_small.jpg" width="240" height="180" /> image</p>'
        >>> Entry.published_objects.get(slug='url').linebreaks_body_for_mobile()
        u'<p><a href="/blog/mobile/spamhamegg/" data-rel="dialog" data-transition="flip">link</a></p>'
        """
        value = self.linebreaks_body()
        for mo in re.finditer('<img src="/site_media/images/.*?>', value):
            tmp = mo.group().replace('_medium', '_small').replace('500', '240').replace('375', '180')
            value = value.replace(mo.group(), tmp)
        for mo in re.finditer('<a href="/blog/.*?>', value):
            tmp = mo.group().replace('="/blog/', '="/blog/mobile/').replace('>', ' data-rel="dialog" data-transition="flip">')
            value = value.replace(mo.group(), tmp)
        return value

    def remove_indent_body(self):
        """
        >>> Entry.published_objects.get(slug='slug').remove_indent_body() == unicode(u'本文')
        True
        """
        pattern = re.compile(u'^　', re.M)
        return re.sub(pattern, '', self.body)




# class RelEntry(models.Model):
#     from_entry = models.ForeignKey(Entry, related_name='from_entries')
#     to_entry = models.ForeignKey(Entry, related_name='to_entries')

#     class Meta:
#         db_table = 'blog_entry_rel_entries'

class PublishedCommentManager(models.Manager):
    def get_query_set(self):
        return super(PublishedCommentManager, self).get_query_set().filter(is_publish=True)


class Comment(models.Model):
    author = models.CharField("投稿者", max_length=50, blank=False)
    body = models.TextField("本文", blank=False)
    created = models.DateTimeField("登録日時", auto_now_add=True)
    is_publish = models.BooleanField("公開設定", blank=False, default=True)

    entry = models.ForeignKey(Entry, related_name='comments', verbose_name="エントリー")

    objects = models.Manager()
    published_objects = PublishedCommentManager()

    class Meta:
        get_latest_by = 'created'
        ordering = ['-created']
        #order_with_respect_to = 'entry'
        verbose_name = 'こめんと'
        verbose_name_plural = 'こめんと'

    def save(self, *args, **kwargs):
        if self.id == None:
            e = self.entry
            e.comment_count += 1
            e.save()
        cache.delete('recent_comments')
        super(Comment, self).save(*args, **kwargs)

    def delete(self):
        e = self.entry
        e.comment_count -= 1
        e.save()
        cache.delete('recent_comments')
        super(Comment, self).delete()


class PublishedAmazonAsamashiManager(models.Manager):
    def get_query_set(self):
        return super(PublishedAmazonAsamashiManager, self).get_query_set().filter(is_publish=True)


class AmazonAsamashi(models.Model):
    asin = models.CharField("ASIN", blank=False, max_length=50)
    comment = models.CharField("コメント", max_length=50, blank=True)
    created = models.DateTimeField("登録日時", auto_now_add=True)
    is_publish = models.BooleanField("トップで紹介", blank=False, default=True)
    priority = models.IntegerField("優先度", blank=False, default=0)
    title = models.CharField("商品名", max_length=200, blank=True, editable=False)

    objects = models.Manager()
    published_objects = PublishedAmazonAsamashiManager()

    class Meta:
        ordering = ['-created', 'priority']
        verbose_name_plural = 'アマゾンあさまし'
        verbose_name = "アマゾンあさまし"

    def __unicode__(self):
        if self.title == None:
            return u"アイテム無し"
        return self.title

    def save(self, *args, **kwargs):
        url = '{http://webservices.amazon.com/AWSECommerceService/2006-11-14}'
        try:
            xml = ElementTree.parse(urllib.urlopen("http://webservices.amazon.co.jp/onca/xml?Service=AWSECommerceService&AWSAccessKeyId=" + settings.AWS_ACCESS_KEY_ID + "&AssociateTag=" + settings.AWS_ASSOCIATE_TAG + "&Operation=ItemLookup&ItemId=" + self.asin + "&ResponseGroup=ItemAttributes&Version=2006-11-14"))
            self.title = str(xml.find(url + 'Items/' + url + 'Item/' + url + 'ItemAttributes/' + url + 'Title').text)
        except:
            self.title = "アイテム無し"
        cache.delete('asamashies_items')

        super(AmazonAsamashi, self).save(*args, **kwargs)


class EntryImage(models.Model):
    description = models.CharField("概要", max_length=200, blank=True)
    created = models.DateTimeField("追加日", auto_now_add=True)
    updated = models.DateTimeField("変更日時", auto_now=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d', height_field='height', width_field='width')
    height = models.PositiveIntegerField(null=True, editable=False)
    width = models.PositiveIntegerField(null=True, editable=False)
    thumb_image = models.CharField(blank=True, max_length=100, editable=False)
    thumb_height = models.PositiveIntegerField(blank=True, null=True, editable=False)
    thumb_width = models.PositiveIntegerField(blank=True, null=True, editable=False)
    medium_image = models.CharField(blank=True, max_length=100, editable=False)
    medium_height = models.PositiveIntegerField(blank=True, null=True, editable=False)
    medium_width = models.PositiveIntegerField(blank=True, null=True, editable=False)
    small_image = models.CharField(blank=True, max_length=100, editable=False)
    small_height = models.PositiveIntegerField(blank=True, null=True, editable=False)
    small_width = models.PositiveIntegerField(blank=True, null=True, editable=False)
    is_publish = models.BooleanField("公開する", blank=False, default=True)

    created_by = models.ForeignKey(User, related_name='entry_images', verbose_name=u"投稿者")
    tags = models.ManyToManyField(EntryTag, related_name='entry_images', verbose_name=u"タグ", blank=True)
    rel_entry_images = models.ManyToManyField('self', verbose_name=u"関連イメージ", blank=True, symmetrical=True)

    class Meta:
        get_latest_by = 'created'
        ordering = ['-created']
        verbose_name = 'しゃしん'
        verbose_name_plural = 'しゃしん'

    def __unicode__(self):
        return self.description + '(' +os.path.basename(smart_unicode(self.image)) + ')'

    def save(self, *args, **kwargs):
        #if not self.id == None:
        # Django 1.1の仕様変更によりとりあえずセーブ
        super(EntryImage, self).save(*args, **kwargs)

        base, ext = os.path.splitext(self.image.field.generate_filename(self.image, self.image.name))
        medium_image = {"path": base + "_medium" + ext, "width": 500, "height": 375}
        small_image = {"path": base + "_small" + ext, "width": 240, "height": 180}
        thumb_image = {"path": base + "_thumb" + ext, "width": 100, "height": 75}
        images = [medium_image, small_image, thumb_image]

        org_img = Image.open(settings.MEDIA_ROOT + "/" + self.image.url).copy()
        try:
            for image in images:
                img = org_img.copy()
                if img.size[0] > image['width'] or img.size[1] > image['height']:
                    if not image['width'] == 100:
                        if img.size[0] < img.size[1]:
                            img.thumbnail((image['height'], image['width']), Image.ANTIALIAS)
                        else:
                            img.thumbnail((image['width'], image['height']), Image.ANTIALIAS)
                    else:
                        img.thumbnail((image['width'], image['height']), Image.ANTIALIAS)

                img.save(settings.MEDIA_ROOT + "/" + image['path'])
                if image['width'] == 500:
                    self.medium_image = image['path']
                    self.medium_width = img.size[0]
                    self.medium_height = img.size[1]
                elif image['width'] == 240:
                    self.small_image = image['path']
                    self.small_width = img.size[0]
                    self.small_height = img.size[1]
                elif image['width'] == 100:
                    self.thumb_image = image['path']
                    self.thumb_width = img.size[0]
                    self.thumb_height = img.size[1]
        except:
            pass

        super(EntryImage, self).save(*args, **kwargs)

    def delete(self):
        medium_image_path = settings.MEDIA_ROOT + "/" + self.medium_image
        thumb_image_path = settings.MEDIA_ROOT + "/" + self.thumb_image
        small_image_path = settings.MEDIA_ROOT + "/" + self.small_image

        images = [medium_image_path, small_image_path, thumb_image_path]
        for image in images:
            if os.path.exists(image):
                os.remove(image)

        super(EntryImage, self).delete()
