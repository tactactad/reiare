# -*- coding: utf-8 -*-
from django.conf import settings

def blog_context(request):
    return {
        'BLOG_TITLE': settings.BLOG_TITLE,
        'BLOG_SUB_TITLE': settings.BLOG_SUB_TITLE,
    }
