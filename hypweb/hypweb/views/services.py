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

class ServiceView(object):

    def __init__(self, request):
        self.request = request
        self.settings = request.registry.settings

    @view_config(route_name='service', renderer='services.mako')
    def service(self):
        login = authenticated_userid(self.request)
        url = urlparse.urlparse(self.request.url)
        services_url = '%s://%s:%s/services/' % (url.scheme, url.hostname, self.settings['hypd_port'])
        ifIndex = self.request.matchdict['ifIndex']

        try:
            r = requests.get('%s%s/' % (services_url, ifIndex))
        except Exception, e:
            self.request.session.flash(e)
            return dict(services='[]', login=login)
        if r.status_code == requests.codes.ok:
            parts = r.headers['Content-Type'].split(';')
            if parts[0] == 'application/json':
                return dict(services=simplejson.dumps(r.json()), login=login)
            else:
                return HTTPNotFound()
        else:
            return HTTPNotFound()

    @view_config(route_name='services', renderer='services.mako')
    def services(self):
        login = authenticated_userid(self.request)
        url = urlparse.urlparse(self.request.url)
        instances_url = '%s://%s:%s/instances/' % (url.scheme, url.hostname, self.settings['hypd_port'])

        try:
            r = requests.get(instances_url)
        except Exception, e:
            self.request.session.flash(e)
            return dict(services='[]', instances=[], login=login)

        if r.status_code != requests.codes.ok:
            return dict(services='[]', instances=[], login=login)
        instances = r.json()
        for instance in instances:
            try:
                r = requests.get('%s%s/interfaces/' %  (instances_url, instance['index']))
            except Exception, e:
                self.request.session.flash(e)
            if r.status_code != requests.codes.ok:
                return dict(services='[]', instances=[], login=login)
            instance['interfaces'] = r.json()

        instance = instances[0]
        interfaces = instance['interfaces']
        interface = interfaces[0]
        
        try:
            r = requests.get('%s://%s:%s/services/%d' % (url.scheme, url.hostname, self.settings['hypd_port'], interface['index']))
        except Exception, e:
            self.request.session.flash(e)
            return dict(services='[]', instances=[], login=login)
        if r.status_code == requests.codes.ok:
            parts = r.headers['Content-Type'].split(';')
            if parts[0] == 'application/json':
                return dict(services=simplejson.dumps(r.json()), instances=instances, login=login)
            else:
                return HTTPNotFound()
        else:
            return HTTPNotFound()
