""" Copyright 2015 Will Boyce """
from __future__ import print_function, unicode_literals

from telegrambot.api.base import APIObject

from telegrambot.api.chat import Chat
from telegrambot.api.media import Audio, Document, Location, PhotoSize, Sticker, Video
from telegrambot.api.user import User


__all__ = ['Message']


class Message(APIObject):
    """
        This object represents a message.


        message_id              int                 Unique message identifier
        date                    int                 Date the message was sent in Unix time
        chat                    Chat                Conversation the message belongs to
        from                    User                (Optional) Sender, can be empty for messages sent to channels
        forward_from            User                (Optional) For forwarded messages, sender of the original message
        forward_date            int                 (Optional) For forwarded messages, date the original message was sent in Unix time
        reply_to_message        Message             (Optional) For replies, the original message. Note that the Message object in this field will not contain further reply_to_message fields even if it itself is a reply.
        text                    str                 (Optional) For text messages, the actual UTF-8 text of the message
        audio                   Audio               (Optional) Message is an audio file, information about the file
        document                Document            (Optional) Message is a general file, information about the file
        photo                   Array of PhotoSize  (Optional) Message is a photo, available sizes of the photo
        sticker                 Sticker             (Optional) Message is a sticker, information about the sticker
        video                   Video               (Optional) Message is a video, information about the video
        voice                   Voice               (Optional) Message is a voice message, information about the file
        caption                 str                 (Optional) Caption for the photo or video
        contact                 Contact             (Optional) Message is a shared contact, information about the contact
        location                Location            (Optional) Message is a shared location, information about the location
        new_chat_participant    User                (Optional) A new member was added to the group, information about them (this member may be the bot itself)
        left_chat_participant   User                (Optional) A member was removed from the group, information about them (this member may be the bot itself)
        new_chat_title          str                 (Optional) A chat title was changed to this value
        new_chat_photo          Array of PhotoSize    (Optional) A chat photo was change to this value
        delete_chat_photo       bool                (Optional) Service message: the chat photo was deleted
        group_chat_created      bool                (Optional) Service message: the group has been created
        supergroup_chat_created bool                (Optional) Service message: the supergroup has been created
        channel_chat_created    bool                (Optional) Service message: the channel has been created
        migrate_to_chat_id      int                 (Optional) The group has been migrated to a supergroup with the specified identifier, not exceeding 1e13 by absolute value
        migrate_from_chat_id    int                 (Optional) The supergroup has been migrated from a group with the specified identifier, not exceeding 1e13 by absolute value
    """
    _api_attrs = (
        ('message_id', int, TypeError),
        ('date', 'date', TypeError),
        ('chat', Chat, TypeError),
        ('from', User, None),
        ('forward_from', User, None),
        ('forward_date', 'date', None),
        ('reply_to_message', 'self', None),
        ('text', str, None),
        ('audio', Audio, None),
        ('document', Document, None),
        ('photo', [PhotoSize], None),
        ('sticker', Sticker, None),
        ('video', Video, None),
        ('caption', str, None),
        ('location', Location, None),
        ('new_chat_participant', User, None),
        ('left_chat_participant', User, None),
        ('new_chat_title', str, None),
        ('new_chat_photo', [PhotoSize], None),
        ('delete_chat_photo', bool, False),
        ('group_chat_created', bool, False),
        ('supergroup_chat_created', bool, False),
        ('channel_chat_created', bool, False),
        ('migrate_to_chat_id', int, None),
        ('migrate_from_chat_id', int, None),
    )

    _api_method = 'send_message'
    _api_payload = (
        'chat_id',
        'text',
        'parse_mode',
        'disable_web_page_preview',
        'reply_to_message_id',
        'reply_markup',
    )

    def __init__(self, api, chat=None, text=None, reply_to_message=None, reply_markup=None):
        super(Message, self).__init__(api)
        if isinstance(chat, Chat):
            self.chat = chat
            self.chat_id = chat.id
        else:
            self.chat_id = chat
        self.text = text
        if isinstance(reply_to_message, Message):
            self.reply_to_message = reply_to_message
            self.reply_to_message_id = reply_to_message.message_id
        else:
            self.reply_to_message_id = reply_to_message
        self.reply_markup = reply_markup

    def forward(self, chat_id=None):
        if chat_id is None:
            chat_id = self.chat_id
        return self.api.forward_message(chat_id=chat_id, from_chat_id=self.chat_id, message_id=self.message_id)

    def reply(self, text, hide_urls=False):
        # TODO: add support here for replying with media payloads (Audio, Video, Photo, etc)
        return Message(api=self.api,
                       chat=self.chat.id,
                       text=text,
                       reply_to_message=self.message_id,
                       ).send(disable_web_page_preview=hide_urls)
