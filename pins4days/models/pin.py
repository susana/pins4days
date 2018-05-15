# -*- coding: utf-8 -*-

from google.appengine.ext import ndb

from attachment import Attachment


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
