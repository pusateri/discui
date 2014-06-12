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
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer

from ..models import *

log = logging.getLogger(__name__)

class DNSView(object):

    def __init__(self, request):
        self.request = request
        self.settings = request.registry.settings

    @view_config(route_name='browse_domains', renderer='browse_domains.mako')
    def dns(self):
        login = authenticated_userid(self.request)
        url = urlparse.urlparse(self.request.url)
        bds_url = '%s://%s:%s/browse_domains/' % (url.scheme, url.hostname, self.settings['hypd_port'])
        domains_url = '%s://%s:%s/domains/' % (url.scheme, url.hostname, self.settings['hypd_port'])

        try:
            r = requests.get(domains_url)
        except Exception, e:
            self.request.session.flash(e)
            return dict(browse_domains='[]', domains='[]', login=login)

        if r.status_code != requests.codes.ok:
            return dict(browse_domains='[]', domains='[]', login=login)
        domains = r.json()

        try:
            r = requests.get(bds_url)
        except Exception, e:
            self.request.session.flash(e)
            return dict(browse_domains='[]', domains='[]', instances=[], login=login)
        if r.status_code == requests.codes.ok:
            parts = r.headers['Content-Type'].split(';')
            if parts[0] == 'application/json':
                return dict(browse_domains=simplejson.dumps(r.json()), domains=simplejson.dumps(domains), login=login)
            else:
                return HTTPNotFound()
        else:
            return HTTPNotFound()
