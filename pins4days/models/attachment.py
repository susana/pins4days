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
