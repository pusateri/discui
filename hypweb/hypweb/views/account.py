import logging
import datetime
import formencode
import socket
import smtplib
import hashlib
import urlparse
from email.mime.text import MIMEText
from pyramid.security import authenticated_userid, remember, forget
from pyramid.httpexceptions import HTTPNotFound, HTTPFound
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer
from pyramid.url import route_url
from pyramid.view import view_config, forbidden_view_config
from pyramid.response import Response

from ..models import *

log = logging.getLogger(__name__)
priv = {'Admin':'admin', 'Upload & View':'upload', 'View':'view'}

invitation = """\
    You have been invited by %s to join the DNS Hyp
    instance %s with %s privileges.

    Please use the following link to finish the registration process.
    %s
"""

class AccountView(object):

    def __init__(self, request):
        self.request = request
        self.settings = request.registry.settings

    @view_config(route_name='login', renderer='home.mako')
    @forbidden_view_config(renderer='home.mako')
    def login(self):
        home = route_url('home', self.request)
        came_from = self.request.params.get('came_from', home)
        
        form = Form(self.request, schema=LoginForm)
        post_data = self.request.POST
        if 'email' in post_data:
            if form.validate():
                email = post_data['email']
                password = post_data['password']
                account = Account.get_by_email(email)
                if account is not None and Account.check_password(email, password):
                    headers = remember(self.request, email)
                    self.request.session.flash(u'Logged in successfully.')
                    return HTTPFound(location=came_from, headers=headers)
                else:
                    self.request.session.flash(u'Email or password incorrect.')
            else:
                self.request.session.flash(u'Email or passowrd not valid.')

        register = Form(self.request, schema=RegisterForm)
        return dict(form=FormRenderer(form), register=FormRenderer(register))

    @view_config(route_name='signout')
    def signout(self):
        self.request.session.flash('You have been signed out.')
        headers = forget(self.request)
        loc = self.request.route_url('login')
        return HTTPFound(location=loc, headers=headers)

    @view_config(route_name='register')
    def register(self):
        self.request.session.flash('Registration not yet active.')
        return HTTPFound(location=self.request.route_url("home"))

    @view_config(route_name='home', renderer='index.mako')
    def index(self):
        login = authenticated_userid(self.request)
        url = urlparse.urlparse(self.request.url)
        summary_url = '%s://%s:%s/summary/' % (url.scheme, url.hostname, self.settings['hypd_port'])
        return dict(login=login, summary_url=summary_url)
        
    def _add_invite(self, email, realm, privilege):
        m = hashlib.md5()
        m.update(realm)
        m.update(email)
        m.update(privilege)
        id = m.hexdigest()
        invite = DBSession.query(Invite).filter(Invite.id == id).first()
        if not invite:
            invite = Invite()
            invite.id = id
            invite.realm = realm
            invite.email = email
            invite.privilege = privilege
            invite.created = datetime.datetime.utcnow()
            DBSession.add(invite)
        return invite.id

    def _add_role(self, realm, account, perm):
        permission = Permission.add_permission(realm, account, perm)

    def _invite_complete(self, invite, realm):
        account = Account.get_by_email(invite.email)
        self._add_role(realm, account, priv[invite.privilege])
        
        #delete invite
        DBSession.delete(invite)

    @view_config(route_name='invite', renderer='account/invite.mako')
    def show_invite(self, id):
        login = authenticated_userid(self.request)
        c = {}
        c.account = None
        c.member = False
        c.invite = DBSession.query(Invite).filter(Invite.id == id).first()
        if c.invite: 
            c.form_errors = None
            c.password = ''
            realm = DBSession.query(Realm) \
                         .filter(Realm.name == c.invite.realm).first()
            c.account = Account.get_by_email(c.invite.email)
            if c.invite.email in auth.realm_users(c.invite.realm):
                c.member = True
            elif c.account:
                self._invite_complete(c.invite, realm)
            elif self.request.method == "POST":
                schema = PasswordForm()
                try:
                    form_result = schema.to_python(self.request.params)
                except formencode.validators.Invalid, error:
                    c.form_result = error.value
                    c.form_errors = error.error_dict or {}
                    log.debug('err: ' + str(error.value))
                    log.debug(str(formencode.validators.Invalid))
                else:
                    #create account
                    users = request.environ['authkit.users']
                    
                    if not c.account:
                        c.account = Account.add_account(users, c.invite.email,
                                                        self.request.params['realname'],
                                                        self.request.params['password1'])
                        self._invite_complete(c.invite, realm)
                    return HTTPFound(location=self.request.route_url("home"))

        return dict(login=login,c=c)

    def _send_invite(self, sender_email, privilege, sender_name):
        c = self.request.tmpl_context
        c.email = self.request.params['email']
        realm = self.request.params['realm']
        c.invite_id = self._add_invite(c.email, realm, privilege)
        inviter = "%s <%s>" % (sender_name, sender_email)
        url = h.url_for('invite', qualified=True, id=c.invite_id)
        msg = MIMEText(invitation % (inviter, realm, privilege, url))
        msg['Subject'] = 'Invitation to join Hyp'
        sender_desc = 'Hyp (from %s)' % sender_email
        sender = '"' + sender_desc + '" <support@bangj.com>'
        msg['From'] = sender
        msg['To'] = c.email

        try:
            s = smtplib.SMTP('jj.bangj.com')
            s.sendmail(sender, [c.email], msg.as_string())
            s.quit()
        except socket.error, (value, msg):
            c.smtp_error = msg
        except smtplib.SMTPException, msg:
            c.smtp_error = msg

    @view_config(route_name='accounts', renderer='account/show.mako') 
    def show(self):
        login = authenticated_userid(self.request)
        account = Account.get_by_email(login)
        form = Form(self.request, schema=RealmForm)
        regen = Form(self.request, schema=RegenerateForm)
        perms = DBSession.query(Permission).filter(Permission.account_id == account.id)
        c = self.request.tmpl_context
        c.snapcount = {}
        c.realms = DBSession.query(Realm).join(Permission).filter(Permission.account_id == account.id)
        for realm in c.realms:
            c.snapcount[realm.id] = DBSession().query(Snapshot).join(Device) \
                                        .filter(Device.realm_id == realm.id).count()

        c.accounts = {}
        accounts = DBSession.query(Account).all()
        for acc in accounts:
            c.accounts[acc.id] = acc

        c.admin_priv = auth.admin_realms(login)
        c.upload_priv = {}
        c.view_priv = {}
        c.users = {}
        c.root_admin = False
        if account.id == 1:
            c.root_admin = True
        root_realm = None

        return dict(form=FormRenderer(form), regen=FormRenderer(regen), login=login, c=c, perms=perms)

    def showparts(self):
        for realm in c.realms:
            c.snapcount[realm.id] = DBSession().query(Snapshot).join(Device) \
                                        .filter(Device.realm_id == realm.id).count()
            if realm.name == '':
                root_realm = realm
            c.users[realm.name] = auth.realm_users(realm.name)
            for user in c.users[realm.name]:
                if not c.admin_priv.get(user):
                    c.admin_priv[user] = auth.admin_realms(user)
                if not c.upload_priv.get(user):
                    c.upload_priv[user] = auth.upload_realms(user)
                if not c.view_priv.get(user):
                    c.view_priv[user] = auth.view_realms(user)
                    
        c.root_admin = root_realm and root_realm.id in c.admin_priv[c.user]
        c.email = ''
        c.invite_id = None
        c.form_errors = None
        c.smtp_error = None
        c.realm = self.request.params.get('realm')
        if self.request.method == "POST":
            schema = EmailForm()
            try:
                form_result = schema.to_python(request.params)
            except formencode.validators.Invalid, error:
                c.form_result = error.value
                c.form_errors = error.error_dict or {}
            else:
                account = c.accounts.get(c.user)
                if account:
                    c.smtp_error = self._send_invite(account.email,
                                                     request.params.get('privilege'),
                                                     account.aka)
                else:
                    self._send_invite(account.email, request.params.get('privilege'), '')
        return dict(login=login, c=c)

    @view_config(route_name='add_realm_form', request_method='POST')
    def add_realm_form(self):
        form = Form(self.request, schema=RealmForm)
        post_data = self.request.POST
        if 'realm_name' in post_data:
            if form.validate():
                realm_name = post_data['realm_name']
                realm_description = post_data['realm_description']
                realm = DBSession.query(Realm).filter(Realm.name == realm_name).first()
                if not realm:
                    realm = Realm.add_realm(realm_name, realm_description)
                    login = authenticated_userid(self.request)
                    account = Account.get_by_email(login)
                    if account:
                        self._add_role(realm, account, 'admin')
                    self.request.session.flash(u'Realm added.')
                else:
                    self.request.session.flash(u'Realm already in use.')
            else:
                self.request.session.flash(u'Realm name or description not valid.')
                    
        return HTTPFound(location=self.request.route_url("accounts"))

    @view_config(route_name='profile', renderer='account/edit.mako')
    def edit_account(self):
        login = authenticated_userid(self.request)
        c={}
        c.account = Account.get_by_email(login)
        if not c.account:
            return HTTPFound(location=self.request.route_url("accounts"))

        users = request.environ['authkit.users']
        if request.method == "POST":
            if request.params.get('submit') == "Update":
                if request.params.get('aka') != c.account.aka:
                    c.account.aka = request.params.get('aka')
                    
                if request.params.get('email') != c.account.email:
                    email = request.params.get('email')
                    try:
                        users.user_set_username(c.account.email, email)
                        c.account.email = email
                    except AuthKitNoSuchUserError, c.error:
                        return HTTPFound(location=self.request.route_url("profile"))
                    except AuthKitError, c.error:
                        return HTTPFound(location=self.request.route_url("profile"))
                        
                if users.user_has_password(c.account.email, request.params.get('oldpassword')):
                    p1 = request.params.get('password1')
                    if len(p1) and p1 == request.params.get('password2'):
                        users.user_set_password(c.account.email, p1)
            return HTTPFound(location=self.request.route_url("accounts"))
        return dict(login=login, c=c)

    @view_config(route_name='remove_from_realm', request_method='POST')
    def remove_account_from_realm(self, id):
        login = authenticated_userid(self.request)
        account = DBSession.query(Account) \
                      .filter(Account.id == id).first()
        if account:
            users = request.environ['authkit.users']
            for role in users.user_roles(account.email):
                privilege, sep, realm_name = role.partition('--')
                if realm_name == request.params.get('realm'):
                    users.user_remove_role(account.email, role)

        return HTTPFound(location=self.request.route_url("accounts"))

    @view_config(route_name='remove_account', request_method='DELETE')
    def remove_account(self, id):
        login = authenticated_userid(self.request)
        account = DBSession.query(Account) \
                      .filter(Account.id == id).first()
        if account:
            users = request.environ['authkit.users']
            if users.user_exists(email):
                users.user_delete(email)
            DBSession.delete(account)
        return HTTPFound(location=self.request.route_url("accounts"))

    @view_config(route_name='regenerate', request_method='POST')
    def regenerate(self):
        login = authenticated_userid(self.request)
        regen = Form(self.request, schema=RegenerateForm)
        post_data = self.request.POST
        realm_id = None
        if 'realm_id' in post_data:
            if regen.validate():
                realm_id = post_data['realm_id']

        realm = DBSession.query(Realm) \
                .filter(Realm.id == realm_id).first()
        if realm:
            realm.makehash()

        return HTTPFound(location=self.request.route_url("accounts"))
