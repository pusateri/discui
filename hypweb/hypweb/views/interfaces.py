import logging
import datetime
import requests
import simplejson
import urlparse
from pyramid.security import authenticated_userid, remember, forget
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from pyramid.url import route_url
from pyramid.view import view_config, forbidden_view_config
from pyramid.response import Response

from ..models import *

log = logging.getLogger(__name__)

class InterfaceView(object):

    def __init__(self, request):
        self.request = request
        self.settings = self.request.registry.settings

    @view_config(route_name='interfaces', renderer='interfaces.mako')
    def interfaces(self):
        url = urlparse.urlparse(self.request.url)
        instances_url = '%s://%s:%s/instances/' % (url.scheme, url.hostname, self.settings['hypd_port'])
        login = authenticated_userid(self.request)
        try:
            r = requests.get(instances_url)
        except Exception, e:
            self.request.session.flash(e)
            return dict(login=login, instances=[])
        if r.status_code == requests.codes.ok:
            parts = r.headers['Content-Type'].split(';')
            if parts[0] == 'application/json':
                return dict(instances=r.json(), login=login, instances_url=instances_url)
            else:
                return HTTPNotFound()
        else:
            return HTTPNotFound()
    
