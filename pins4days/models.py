# -*- coding: utf-8 -*-

from google.appengine.ext import ndb
from lib.pybcrypt import bcrypt


# Although the Address instances are defined using the same syntax as for model classes, they are not full-fledged entities. They don't have their own keys in Cloud Datastore. They cannot be retrieved independently of the Contact entity to which they belong
class Attachment(ndb.Model):
    from_url = ndb.StringProperty('frurl')
    image_url = ndb.StringProperty('imurl')
    original_url = ndb.StringProperty('ogurl')
    text = ndb.StringProperty('tx')


class Pin(ndb.Model):
    text = ndb.TextProperty('tx')
    author_id = ndb.StringProperty('aid')
    pinner_id = ndb.StringProperty('pid')
    channel_id = ndb.StringProperty('cid')
    pinned_ts = ndb.IntegerProperty('pts')
    created_ts = ndb.IntegerProperty('cts')
    attachments = ndb.StructuredProperty(Attachment, name='a', repeated=True)
    attachments_ts = ndb.StringProperty('ats') # ts along with the channel idcan be used to recreate the permalink

    @classmethod
    def query_user(cls, user_id):
        return cls.query(getattr(Pin, 'author_id') == user_id).order(-cls.created_ts)

    @classmethod
    def query_all(cls):
        return cls.query().order(-cls.created_ts)


class User(ndb.Model):
    # key.id is set to the username to maintain unique constraint
    password = ndb.StringProperty('pw', required=True)

    @staticmethod
    def compare_passwords(stored_pw, unencrypted_pw):
        return bcrypt.hashpw(unencrypted_pw, stored_pw) == stored_pw

    @staticmethod
    def encrypt_password(password):
        return bcrypt.hashpw(password, bcrypt.gensalt())

    @classmethod
    def init_with_encryption(cls, **kwargs):
        if not cls.get_by_id(kwargs['id']):
            kwargs['password'] = cls.encrypt_password(kwargs['password'])
            user = cls(**kwargs)
            user.put()

    @classmethod
    def update_password(username, new_pw):
        user = Key(cls, username).get()
        user.password = cls.encrypt_password(new_pw)
        user.put()

    @classmethod
    def login(cls, username, submitted_pw):
        user = cls.get_by_id(username)
        if user is None:
            raise EntityDoesNotExist(
                "User with username '{}' does not exist.".format(username))
        stored_pw = user.password
        is_correct_pw = cls.compare_passwords(stored_pw, submitted_pw)
        if not is_correct_pw:
            raise IncorrectPassword
        return user


class EntityDoesNotExist(Exception):
    pass

class IncorrectPassword(Exception):
    pass
