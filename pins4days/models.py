# -*- coding: utf-8 -*-
"""NDB models for pins, attachments and Pins4Days users."""

from google.appengine.ext import ndb
from lib.pybcrypt import bcrypt


class Attachment(ndb.Model):

    """Represents a Slack message's attachments. These can be images,
    external URLs, and more. This model is a simplification of Slack's
    attachment model, only storing images and text from attachments.

    Note to self about 'StructuredProperty's:
    "Although the Address instances are defined using the same syntax as for
    model classes, they are not full-fledged entities. They don't have their
    own keys in Cloud Datastore. They cannot be retrieved independently of
    the Contact entity to which they belong.""

    Attributes:
        from_url (StringProperty):
        image_url (StringProperty): An image URL. Could be extracted from
        an HTML page, or simply the URL that was posted directly into a message.
        original_url (StringProperty): The URL that was posted. Could be an
        image, HTML page, etc.
        text (StringProperty): Optional. Text from an attachment. E.g. article
        intro/blurb.
    """

    from_url = ndb.StringProperty('frurl')
    image_url = ndb.StringProperty('imurl')
    original_url = ndb.StringProperty('ogurl')
    text = ndb.StringProperty('tx')


class Pin(ndb.Model):

    """Represents a Slack pinned message. Each message can contain text and
    attachments (see Attachment above).

    Attributes:
        attachments (StructuredProperty): A series of attachments associated
        with the image. Could be images, links, etc.
        attachments_ts (IntegerProperty): Timestamp of when the attachments were created.
        author_id (StringProperty): User ID of the person who authored the message.
        channel_id (StringProperty): ID of the channel that the message was pinned in.
        created_ts (IntegerProperty): (Todo: verify) Timestamp of when the message was
        created.
        pinned_ts (IntegerProperty): Timestamp of when the message was pinned.
        pinner_id (StringProperty): ID of the user that pinned the message.
        text (TextProperty): Pinned message's text.
    """

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
        """Creates the query for fetching a user's pins in reverse chronological
        order.

        Args:
            user_id (str): The user's Slack ID.

        Returns:
            Query:
        """
        return cls.query(getattr(Pin, 'author_id') == user_id).order(-cls.created_ts)

    @classmethod
    def query_all(cls):
        """Creates the query for fetching all pins in reverse chronological
        order.

        Returns:
            Query:
        """
        return cls.query().order(-cls.created_ts)


class User(ndb.Model):

    """Represents a Pins4Days app user.

    Attributes:
        password (StringProperty): The user's password. ENCRYPT BEFORE STORING!
        See User.encrypt_password() and User.init_with_encryption().
    """

    # The User entity's key.id is set to the username to maintain unique
    # constraint.
    password = ndb.StringProperty('pw', required=True)

    @staticmethod
    def compare_passwords(stored_pw, unencrypted_pw):
        """Compares a stored password with an unencrypted password to see if
        they match.

        Args:
            stored_pw (str): The password that is currently stored in the DB.
            unencrypted_pw (str): An unencrypted password to compare to the
            stored password.

        Returns:
            bool: Returns True if the passwords match. False, otherwise.
        """
        return bcrypt.hashpw(unencrypted_pw, stored_pw) == stored_pw

    @staticmethod
    def encrypt_password(password):
        """Encrypts (bcrypt) a given password.

        Args:
            password (str): The password to encrypt.

        Returns:
            str: The encrypted password.
        """
        return bcrypt.hashpw(password, bcrypt.gensalt())

    @classmethod
    def init_with_encryption(cls, **kwargs):
        """Creates a new User, including encrypting their password, if that
        User doesn't already exist. Otherwise, does nothing.

        Args:
            **kwargs: The keyword args accepts by the User NDB model. These
            are currently: password.
        """
        if not cls.get_by_id(kwargs['id']):
            kwargs['password'] = cls.encrypt_password(kwargs['password'])
            user = cls(**kwargs)
            user.put()

    @classmethod
    def update_password(cls, username, new_pw):
        """Updates an existing User's password.

        Args:
            username (User): The user that will get the new password.
            new_pw (str): The new password, unencrypted.
        """
        user = ndb.Key(cls, username).get()
        user.password = cls.encrypt_password(new_pw)
        user.put()

    @classmethod
    def login(cls, username, submitted_pw):
        """Essentially looks for an existing User based on the given username
        and submitted_pw.

        Args:
            username (str): The username.
            submitted_pw (str): The password that corresponds with the given
            username.

        Returns:
            User:

        Raises:
            EntityDoesNotExist: Thrown if the User does not exist.
            IncorrectPassword: Thrown is the User exists but the wrong password
            is given.
        """
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
    """Should be thrown when an entity does not exist."""
    pass


class IncorrectPassword(Exception):
    """Should be thrown when an incorrect password is supplied."""
    pass
