from sqlalchemy import Column, ForeignKey, UniqueConstraint
from sqlalchemy.types import DateTime, Integer, String, Unicode
from sqlalchemy.ext.declarative import declarative_base
import datetime

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    synonym,
    )

from zope.sqlalchemy import ZopeTransactionExtension
import cryptacular.bcrypt
import formencode
from pyramid.security import Allow, Everyone, Authenticated

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

crypt = cryptacular.bcrypt.BCRYPTPasswordManager()

def hash_password(password):
    return unicode(crypt.encode(password))

def groupfinder(userid, request):
    return ['admin', 'upload', 'view']

# permissions: admin, upload, view
class RootFactory(object):
    __acl__ = [
        (Allow, Authenticated, 'view'),
        (Allow, 'admin', 'admin'),
        (Allow, 'upload', 'upload'),
        (Allow, 'view', 'view'),
    ]
    def __init__(self, request):
        pass

class Realm(Base):
    __tablename__ = 'realms'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    display_name = Column(String)
    created = Column(DateTime, nullable=False)
    post_hash = Column(String, nullable=False, unique=True)

    @classmethod
    def add_realm(self, name, display_name):
        realm = Realm()
        realm.name = name
        realm.display_name = display_name
        realm.created = datetime.datetime.utcnow()
        realm.makehash()
        DBSession.add(realm)
        return realm

    def makehash(self):
        m = hashlib.md5()
        m.update(self.name)
        m.update(self.display_name)
        m.update(str(datetime.datetime.utcnow()))
        self.post_hash = m.hexdigest()

class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    aka = Column(String)
    created = Column(DateTime, nullable=False)
    _password = Column('password', Unicode(60))

    def _get_password(self):
        return self._password

    def _set_password(self, password):
        self._password = hash_password(password)

    password = property(_get_password, _set_password)
    password = synonym('_password', descriptor=password)

    def __init__(self, email, password, aka):
        self.email = email
        self.password = password
        self.aka = aka
        self.created = datetime.datetime.utcnow()

    @classmethod
    def get_by_email(cls, email):
        return DBSession.query(cls).filter(cls.email == email).first()

    @classmethod
    def check_password(cls, email, password):
        account = cls.get_by_email(email)
        if not account:
            return False
        return crypt.check(account.password, password)

class Invite(Base):
    __tablename__ = 'invites'

    id = Column(String, primary_key=True, unique=True)
    email = Column(String, nullable=False)
    realm = Column(String)
    privilege = Column(String)
    created = Column(DateTime, nullable=False)

class Permission(Base):
    __tablename__ = 'permissions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    realm_id = Column(Integer, ForeignKey('realms.id'))
    account_id = Column(Integer, ForeignKey('accounts.id'))
    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False)
    value = Column(String)  # admin, upload, view
    
    @classmethod
    def add_permission(self, realm, account, value):
        p = Permission()
        p.realm_id = realm.id
        p.account_id = account.id
        p.created = datetime.datetime.utcnow()
        p.modified = p.created
        p.value = value
        DBSession.add(p)
        return p


class EmailForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    email = formencode.validators.Email(not_empty=True)

class PasswordForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    realname = formencode.validators.String(not_empty=True)
    password1 = formencode.validators.String(not_empty=True)
    password2 = formencode.validators.String(not_empty=True)
    chained_validators = [formencode.validators.FieldsMatch('password1', 'password2')]

class LoginForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    email = formencode.validators.Email(not_empty=True)
    password = formencode.validators.String(not_empty=True)

class RegisterForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True

class SearchForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True

class RealmForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    realm_name = formencode.validators.String(not_empty=True)
    realm_description = formencode.validators.String(not_empty=True)

class RegenerateForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True

class QueryForm(formencode.Schema):
    allow_extra_fields = True
    filter_extra_fields = True
    ifIndex = formencode.validators.Int(not_empty=True)