# -*- coding: utf-8 -*-

from google.appengine.ext import ndb


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
        author_id (StringProperty): User ID of the person who authored the message.
        channel_id (StringProperty): ID of the channel that the message was pinned in.
        created_ts (IntegerProperty): (Todo: verify) Timestamp of when the message was
        created.
        pinned_ts (IntegerProperty): Timestamp of when the message was pinned.
        pinner_id (StringProperty): ID of the user that pinned the message.
        text (TextProperty): Pinned message's text.
        ts (StringProperty):
    """

    text = ndb.TextProperty('tx')
    author_id = ndb.StringProperty('aid')
    pinner_id = ndb.StringProperty('pid')
    channel_id = ndb.StringProperty('cid')
    pinned_ts = ndb.IntegerProperty('pts')
    created_ts = ndb.IntegerProperty('cts')
    attachments = ndb.StructuredProperty(Attachment, name='a', repeated=True)
    ts = ndb.StringProperty('ts') # ts along with the channel id can be used to recreate the permalink

    @staticmethod
    def build_key_id(channel_id, ts):
        """Creates the unique Pin ID which is based on the channel id and
        creation timestamp which is sent as a float cast as a string.

        Args:
            channel_id (string): The channel the message originated from.
            ts (string): Creation timestamp as a float cast to a string.

        Returns:
            Key:
        """
        return '_'.join([channel_id, ts])

    @classmethod
    def create(cls, **kwargs):
        """Creates a Pin in the database.

        Args:
            **kwargs: The Pin properties.

        Returns:
            Key: If the Pin already exists, the key for that Pin is returned.
        """
        key_id = Pin.build_key_id(kwargs['channel_id'], kwargs['ts'])
        kwargs['id'] = key_id
        pin = cls(**kwargs)
        return pin.put()

    @classmethod
    def query_user(cls, user_id):
        """Creates the query for fetching a user's pins in reverse chronological
        order.

        Args:
            user_id (str): The user's Slack ID.

        Returns:
            Query
        """
        return cls.query(getattr(Pin, 'author_id') == user_id).order(-cls.created_ts)

    @classmethod
    def query_all(cls):
        """Creates the query for fetching all pins in reverse chronological
        order.

        Returns:
            Query
        """
        return cls.query().order(-cls.created_ts)
