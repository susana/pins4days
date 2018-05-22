# -*- coding: utf-8 -*-

import unittest
import json
import os

from datastore_test_case import DatastoreTestCase
from pins4days.event import PinnedMessage
from pins4days.event import MessageAttachment
from pins4days.models.pin import Pin


def path(subpath):
    return os.path.realpath(os.path.join(
        os.getcwd(),
        os.path.dirname(__file__),
        subpath))


class MessageAttachmentTestCase(unittest.TestCase):

    def setUp(self):
        super(MessageAttachmentTestCase, self).setUp()
        with open(path('data/attachment_image.json')) as f:
            self.attachment_image = json.load(f)
        with open(path('data/attachment_link.json')) as f:
            self.attachment_link = json.load(f)


    def test_image_attachment(self):
        attachment = MessageAttachment.factory(self.attachment_image)
        expected = {
            'from_url': u'https://ap.rdcpix.com/1914806510/dc09f00136ec630d5a680af812cde442l-m16xd-w1020_h770_q80.jpg',
            'image_url': u'https://ap.rdcpix.com/1914806510/dc09f00136ec630d5a680af812cde442l-m16xd-w1020_h770_q80.jpg',
            'original_url': u'https://ap.rdcpix.com/1914806510/dc09f00136ec630d5a680af812cde442l-m16xd-w1020_h770_q80.jpg',
            'text': None
        }
        self.assertEquals(expected, attachment.to_dict())

    def test_link_attachment(self):
        attachment = MessageAttachment.factory(self.attachment_link)
        expected = {
            'from_url': u'https://medium.com/basecs/less-repetition-more-dynamic-programming-43d29830a630',
            'image_url': u'https://cdn-images-1.medium.com/max/1200/1*Y1IuqrkoDWLlfz_BSaesGQ.jpeg',
            'original_url': u'https://medium.com/basecs/less-repetition-more-dynamic-programming-43d29830a630',
            'text': u'One of the running themes throughout this series has been the idea of making large, complex problems, which at first may seem super \u2026'
        }
        self.assertDictEqual(expected, attachment.to_dict())


class PinnedMessageTestCase(DatastoreTestCase):

    def setUp(self):
        self.maxDiff = None
        super(PinnedMessageTestCase, self).setUp()
        with open(path('data/pin_added_image.json')) as f:
            self.pin_added_image = json.load(f)
        with open(path('data/pin_added_link.json')) as f:
            self.pin_added_link = json.load(f)
        with open(path('data/pin_added_message.json')) as f:
            self.pin_added_message = json.load(f)
        with open(path('data/pin_added_multi.json')) as f:
            self.pin_added_multi = json.load(f)

    def test_image_pin(self):
        pin = PinnedMessage.factory(self.pin_added_image)
        expected = {
            'author_id': u'user-0',
            'pinner_id': u'authed-user-0',
            'channel_id': u'pinned-to-0',
            'pinned_ts': 1525828511,
            'created_ts': 1525828511,
            'text': u'<https://ap.rdcpix.com/1914806510/dc09f00136ec630d5a680af812cde442l-m16xd-w1020_h770_q80.jpg>',
            'attachments': [
                {
                    'from_url': u'https://ap.rdcpix.com/1914806510/dc09f00136ec630d5a680af812cde442l-m16xd-w1020_h770_q80.jpg',
                    'image_url': u'https://ap.rdcpix.com/1914806510/dc09f00136ec630d5a680af812cde442l-m16xd-w1020_h770_q80.jpg',
                    'original_url': u'https://ap.rdcpix.com/1914806510/dc09f00136ec630d5a680af812cde442l-m16xd-w1020_h770_q80.jpg',
                    'text': None
                }
            ],
            'ts': u'1525815858.000179'
        }
        self.assertEquals('pinned-to-0_1525815858.000179', pin.key.id())
        self.assertDictEqual(expected, pin.to_dict())

    def test_link_pin(self):
        pin = PinnedMessage.factory(self.pin_added_link)
        expected = {
            'author_id': u'authed-user-0',
            'pinner_id': u'authed-user-0',
            'channel_id': u'channel-id-0',
            'pinned_ts': 1525829853,
            'created_ts': 1525829853,
            'text': u'<https://medium.com/basecs/less-repetition-more-dynamic-programming-43d29830a630>',
            'attachments': [
                {
                    'from_url': u'https://medium.com/basecs/less-repetition-more-dynamic-programming-43d29830a630',
                    'image_url': u'https://cdn-images-1.medium.com/max/1200/1*Y1IuqrkoDWLlfz_BSaesGQ.jpeg',
                    'original_url': u'https://medium.com/basecs/less-repetition-more-dynamic-programming-43d29830a630',
                    'text': u'One of the running themes throughout this series has been the idea of making large, complex problems, which at first may seem super \u2026'
                }
            ],
            'ts': u'1525829847.000217'
        }
        self.assertEquals('channel-id-0_1525829847.000217', pin.key.id())
        self.assertDictEqual(expected, pin.to_dict())

    def test_message_pin(self):
        pin = PinnedMessage.factory(self.pin_added_message)
        expected = {
            'author_id': u'user-0',
            'pinner_id': u'authed-user-0',
            'channel_id': u'pinned-to-0',
            'pinned_ts': 1525827355,
            'created_ts': 1525827355,
            'text': u"How do you make a round circle with a square knife? That's your challenge for the day.",
            'attachments': [],
            'ts': "1525813275.000339"
        }
        self.assertEquals('pinned-to-0_1525813275.000339', pin.key.id())
        self.assertDictEqual(expected, pin.to_dict())

    def test_multi_pin(self):
        pin = PinnedMessage.factory(self.pin_added_multi)
        expected = {
            'author_id': u'authed-user-0',
            'pinner_id': u'authed-user-0',
            'channel_id': u'channel-id-0',
            'pinned_ts': 1525831523,
            'created_ts': 1525831523,
            'text': u"<https://medium.com/basecs/less-repetition-more-dynamic-programming-43d29830a630>\n<http://www.catster.com/wp-content/uploads/2017/08/A-fluffy-cat-looking-funny-surprised-or-concerned.jpg>\nblah blah kowpkfwiq",
            'attachments': [
                {
                    'from_url': u'https://medium.com/basecs/less-repetition-more-dynamic-programming-43d29830a630',
                    'image_url': u'https://cdn-images-1.medium.com/max/1200/1*Y1IuqrkoDWLlfz_BSaesGQ.jpeg',
                    'original_url': u'https://medium.com/basecs/less-repetition-more-dynamic-programming-43d29830a630',
                    'text': u'One of the running themes throughout this series has been the idea of making large, complex problems, which at first may seem super'
                },
                {
                    'from_url': u'http://www.catster.com/wp-content/uploads/2017/08/A-fluffy-cat-looking-funny-surprised-or-concerned.jpg',
                    'image_url': u'http://www.catster.com/wp-content/uploads/2017/08/A-fluffy-cat-looking-funny-surprised-or-concerned.jpg',
                    'original_url': u'http://www.catster.com/wp-content/uploads/2017/08/A-fluffy-cat-looking-funny-surprised-or-concerned.jpg',
                    'text': None
                }
            ],
            'ts': u'1525831511.000182'
        }
        self.assertEquals('channel-id-0_1525831511.000182', pin.key.id())
        self.assertDictEqual(expected, pin.to_dict())


if __name__ == '__main__':
    unittest.main()
