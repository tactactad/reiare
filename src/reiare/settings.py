# -*- coding: utf-8 -*-
# Django settings for reiare project.

#DEBUG = False
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = ''#'postgresql_psycopg2'           # 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = ''             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

DEFAULT_CHARSET = 'utf-8'

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'Asia/Tokyo'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'ja'

SITE_ID = 1

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/home/username/site_media'

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.csrf.middleware.CsrfMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.middleware.cache.CacheMiddleware',
    'django.middleware.doc.XViewMiddleware',
    #'django.middleware.debug.DBDebugMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'reiare.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates".
    # Always use forward slashes, even on Windows.
    #'/home/username/reiare/templates'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'blog',
    'django.contrib.flatpages',
    'django.contrib.markup',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'blog.context.blog_context',
)

BLOG_TITLE = ''
BLOG_SUB_TITLE = ''
BLOG_DESCRIPTION = ''
RSS_NUM = 10
PAGINATE_NUM = 20
SIDEBAR_ENTRIES_NUM = 10

MAIL_CHARSET = 'iso-2022-jp'
BLOG_MASTER_EMAIL = ''
BLOG_HOST_URL = ''

DEFAULT_FROM_EMAIL = ''
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
SERVER_EMAIL = ''

AWS_ACCESS_KEY_ID = ''
AWS_ASSOCIATE_TAG = ''

SHOW_TOP_SIDEBAR = 'True'
SHOW_ASAMASHIES = 'True'
SHOW_GOOGLE_SEARCH = 'True'

SHOW_BANNERS = 'True'

SHOW_TOPIC = 'True'
SHOW_SPOT_ASAMASHI = 'True'
SHOW_PROFILE = 'True'
SHOW_ASAMASHISITE_LINKS = 'True'

LASTFM_ID = ''

CACHE_BACKEND = 'db://django_reiare_cache'

# 個別設定を外部ファイルからインポート
from reiare_settings import *

if DEBUG:
    # import logging
    # logging.basicConfig(
    #     level = logging.DEBUG,
    #     format = '%(asctime)s %(levelname)s %(message)s',)
        # filename = '/tmp/reiare.log',
        # filemode = 'w')

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
            }
        }
