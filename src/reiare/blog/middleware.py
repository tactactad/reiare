import re

from django.shortcuts import redirect

class RedirectSmartPhoneMiddleware(object):
    def process_request(self, request):
        if request.META.has_key('HTTP_USER_AGENT') and \
                re.search('iPod|iPhone|Android|BlackBerry|Windows Phone|Symbian|Nintendo 3DS',
                          request.META['HTTP_USER_AGENT']) and \
                not re.match('/blog/mobile', request.path):
            return redirect(request.path.replace('/blog/', '/blog/mobile/', 1))
        else:
            return None
