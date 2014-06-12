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

class QueryView(object):

    def __init__(self, request):
        self.request = request
        self.settings = request.registry.settings

    @view_config(route_name='queries', renderer='queries.mako')
    def queries(self):
        login = authenticated_userid(self.request)
        url = urlparse.urlparse(self.request.url)
        instances_url = '%s://%s:%s/instances/' % (url.scheme, url.hostname, self.settings['hypd_port'])

        try:
            r = requests.get(instances_url)
        except Exception, e:
            self.request.session.flash(e)
            return dict(queries='[]', instances=[], login=login)

        if r.status_code != requests.codes.ok:
            return dict(queries='[]', instances=[], login=login)
        instances = r.json()
        for instance in instances:
            try:
                r = requests.get('%s%s/interfaces/' %  (instances_url, instance['index']))
            except Exception, e:
                self.request.session.flash(e)
            if r.status_code != requests.codes.ok:
                return dict(queries='[]', instances=[], login=login)
            instance['interfaces'] = r.json()

        try:
            r = requests.get('%s://%s:%s/queries/' % (url.scheme, url.hostname, self.settings['hypd_port']))
        except Exception, e:
            self.request.session.flash(e)
            return dict(queries='[]', instances=[], login=login)
        if r.status_code == requests.codes.ok:
            parts = r.headers['Content-Type'].split(';')
            if parts[0] == 'application/json':
                return dict(queries=simplejson.dumps(r.json()), instances=instances, login=login)
            else:
                return HTTPNotFound()
        else:
            return HTTPNotFound()
