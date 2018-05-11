# -*- coding: utf-8 -*-

from google.appengine.ext import ndb


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
