# -*- coding: utf-8 -*-

import logging
from models import Pin
from models import Attachment


class PinEvent(object):
    @staticmethod
    def factory(event):
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
    @staticmethod
    def factory(attachment):
        return Attachment(
            from_url=attachment['from_url'] if 'from_url' in attachment else None,
            image_url=attachment['image_url'] if 'image_url' in attachment else None,
            original_url=attachment['original_url'] if 'original_url' in attachment else None,
            text=attachment['text'] if 'text' in attachment else None)
