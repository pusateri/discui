from pyramid.config import Configurator
from pyramid_beaker import session_factory_from_settings
from sqlalchemy import engine_from_config

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from .models import (
    DBSession,
    Base,
    groupfinder,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    
    authentication_policy = AuthTktAuthenticationPolicy('com.bangj.SecRet', callback=groupfinder)
    authorization_policy = ACLAuthorizationPolicy()

    config = Configurator(settings=settings, root_factory='hypweb:models.RootFactory')
    config.set_authentication_policy(authentication_policy)
    config.set_authorization_policy(authorization_policy)
    config.include('pyramid_beaker')

    session_factory = session_factory_from_settings(settings)
    config.set_session_factory(session_factory)

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('invite', '/invite/{id}')
    config.add_route('accounts', '/accounts')
    config.add_route('profile', '/accounts/edit')
    config.add_route('add_realm_form', '/add_realm_form')
    config.add_route('regenerate', '/accounts/regenerate')
    config.add_route('remove_from_realm', '/accounts/remove_from_realm/{id}')
    config.add_route('signout', '/signout')
    config.add_route('register', '/register')
    config.add_route('remove_account', '/accounts/remove/{id}')

    config.add_route('summary', '/'),
    config.add_route('interfaces', '/interfaces'),
    config.add_route('browse_domains', '/browse_domains/'),
    config.add_route('queries', '/queries'),
    config.add_route('service', '/services/{ifIndex}'),
    config.add_route('services', '/services/'),
    config.add_route('domains', '/domains/'),
    config.add_route('debug', '/debug'),
    config.add_route('feedback', '/'),

    config.scan()
    return config.make_wsgi_app()
