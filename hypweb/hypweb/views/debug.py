import logging
import datetime
import urlparse
from pyramid.security import authenticated_userid, remember, forget
from pyramid.url import route_url
from pyramid.view import view_config, forbidden_view_config
from pyramid.response import Response

from ..models import *

log = logging.getLogger(__name__)

class DebugView(object):

    def __init__(self, request):
        self.request = request
        self.settings = self.request.registry.settings

    @view_config(route_name='debug', renderer='debug.mako')
    def debug(self):
        login = authenticated_userid(self.request)
        url = urlparse.urlparse(self.request.url)
        debug_url = '%s://%s:%s/debug/' % (url.scheme, url.hostname, self.settings['hypd_port'])
        stats_url = '%s://%s:%s/stats/1/' % (url.scheme, url.hostname, self.settings['hypd_port'])
        hosts_url = '%s://%s:%s/hosts/' % (url.scheme, url.hostname, self.settings['hypd_port'])
        return dict(login=login, debug_url=debug_url, stats_url=stats_url, hosts_url=hosts_url)
        
    
