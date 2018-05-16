# -*- coding: utf-8 -*-
"""Factory classes for creating pinsdays.models.pin.Pin and
pinsdays.models.pin.Attachment.
"""

import logging
from models.pin import Pin
from models.pin import Attachment


class PinnedMessage(object):

    """Creates a Pin with Attachments based on the pin_added event sent by
    the Slack events API.
    """

    @staticmethod
    def factory(event):
        """Creates a Pin with Attachments based on the pin_added event sent by
        the Slack events API.

        Args:
            event (dict): A dict representation of the JSON sent by the Slack
            events API upon the creation of a pin_added event.

        Returns:
            pins4days.models.pin.Pin: A Pin model.
        """
        message = event['event']['item']['message']
        pinned_info = event['event']['pinned_info']
        attachments = message['attachments'] if 'attachments' in message else []
        attachment_entities = [MessageAttachment.factory(a) for a in attachments]
        pin = Pin(
            text=message['text'],
            author_id=message['user'],
            pinner_id=pinned_info['pinned_by'],
            channel_id=pinned_info['channel'],
            pinned_ts=pinned_info['pinned_ts'],
            created_ts=event['event']['item']['created'],
            attachments=attachment_entities,
            attachments_ts=message['ts'])
        pin.put()
        return pin


class MessageAttachment(object):

    """Creates Attachments based on the pin_added event sent by the Slack
    events API.
    """

    @staticmethod
    def factory(attachment):
        """Creates Attachments based on the pin_added event sent by the Slack
        events API.

        Args:
            attachment (dict): A portion of the JSON sent by the Slack events
            API upon the creation of a pin_added event. This dict should
            contain only the data for a single attachment. It can be
            accessed from the event JSON/dict like so:
            e.g. event['event']['item']['message']['attachments'][0]

        Returns:
            pins4days.models.attachment.Attachment: An Attachmnent model.
        """
        return Attachment(
            from_url=attachment['from_url'] if 'from_url' in attachment else None,
            image_url=attachment['image_url'] if 'image_url' in attachment else None,
            original_url=attachment['original_url'] if 'original_url' in attachment else None,
            text=attachment['text'] if 'text' in attachment else None)
