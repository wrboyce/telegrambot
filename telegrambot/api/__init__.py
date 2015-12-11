""" Copyright 2015 Will Boyce """
from __future__ import print_function, unicode_literals

import os

import requests

from telegrambot.exceptions import TelegramBadRequestError
from telegrambot.logger import getLogger

from telegrambot.api.base import APIObject

from .chat import Chat
from .keyboards import ReplyKeyboardMarkup, ReplyKeyboardHide, ForceReply
from .media import Audio, Contact, Document, File, Location, PhotoSize, Sticker, Video, Voice
from .message import Message
from .user import User


__all__ = ['Chat',
           'ReplyKeyboardMarkup', 'ReplyKeyboardHide', 'ForceReply',
           'Audio', 'Contact', 'Document', 'File', 'Location', 'PhotoSize', 'Sticker', 'Video', 'Voice',
           'Message',
           'User',
           'TelegramAPIMixin']


class TelegramAPIMixin(object):
    BASE_URL = 'https://api.telegram.org/bot'

    def __init__(self, cfg):
        self.cfg = cfg
        self.base_url = '{}{}:{}'.format(self.BASE_URL, cfg.core.bot_id, cfg.core.token)

    @property
    def logger(self):
        class_path = '.'.join([self.__class__.__module__, self.__class__.__name__])
        if not class_path.startswith('telegrambot'):
            class_path = 'telegrambot.{}'.format(class_path)
        return getLogger(class_path)

    def _get(self, method, payload=None):
        url = '{}/{}'.format(self.base_url, method)
        data = requests.get(url, params=payload).json()
        if not data['ok']:
            raise TelegramBadRequestError('[{}] {}'.format(data['error_code'], data['description']))
        return data['result']

    def _post(self, method, payload=None, files=None):
        url = '{}/{}'.format(self.base_url, method)
        data = requests.post(url, params=payload, files=files).json()
        if not data['ok']:
            raise TelegramBadRequestError('[{}] {}'.format(data['error_code'], data['description']))
        return data['result']

    def get_me(self):
        """
            A simple method for testing your bot's auth token. Requires no parameters.
            Returns basic information about the bot in form of a User object.
        """
        return User.from_api(self, **self._get('getMe'))

    def send_message(self, text, chat_id, reply_to_message_id=None, disable_web_page_preview=False, reply_markup=None):
        """
            Use this method to send text messages. On success, the sent Message is returned.
        """
        self.logger.info('sending message "%s"', format(text.replace('\n', '\\n')))
        payload = dict(text=text,
                       chat_id=chat_id,
                       reply_to_message_id=reply_to_message_id,
                       disable_web_page_preview=disable_web_page_preview,
                       reply_markup=reply_markup)
        return Message.from_api(self, **self._get('sendMessage', payload))

    def forward_message(self, chat_id, from_chat_id, message_id):
        """
            Use this method to forward messages of any kind. On success, the sent Message is returned.
        """
        self.logger.info('forwarding message %s from %s to %s', message_id, from_chat_id, chat_id)
        payload = dict(chat_id=chat_id,
                       from_chat_id=from_chat_id,
                       message_id=message_id)
        return Message.from_api(self, **self._get('forwardMessage', payload))

    def send_photo(self, chat_id, photo, caption=None, reply_to_message_id=None, reply_markup=None):
        """
            Use this method to send photos. On success, the sent Message is returned.
        """
        self.logger.info('send photo %s', photo)
        payload = dict(chat_id=chat_id,
                       caption=caption,
                       reply_to_message_id=reply_to_message_id,
                       reply_markup=reply_markup)
        files = dict(photo=open(photo, 'rb'))
        return Message.from_api(self, **self._post('sendPhoto', payload, files))

    def send_audio(self, chat_id, audio, duration=None, performer=None, title=None, reply_to_message_id=None, reply_markup=None):
        """
            Use this method to send audio files, if you want Telegram clients to display them in the music player.
            Your audio must be in the .mp3 format. On success, the sent Message is returned. Bots can currently send
            audio files of up to 50 MB in size, this limit may be changed in the future.

            For backward compatibility, when the fields title and performer are both empty and the mime-type of the
            file to be sent is not audio/mpeg, the file will be sent as a playable voice message. For this to work,
            the audio must be in an .ogg file encoded with OPUS.

            This behavior will be phased out in the future.
            For sending voice messages, use the send_voice method instead.
        """
        self.logger.info('sending audio payload %s', audio)
        payload = dict(chat_id=chat_id,
                       duration=duration,
                       performer=performer,
                       title=title,
                       reply_to_message_id=reply_to_message_id,
                       reply_markup=reply_markup)
        files = dict(audio=open(audio, 'rb'))
        return Message.from_api(self, **self._post('sendAudio', payload, files))

    def send_document(self, chat_id=None, document=None, reply_to_message_id=None, reply_markup=None):
        """
            Use this method to send general files. On success, the sent Message is returned.
            Bots can currently send files of any type of up to 50 MB in size, this limit may be changed in the future.
        """
        payload = dict(chat_id=chat_id,
                       reply_to_message_id=reply_to_message_id,
                       reply_markup=reply_markup)
        files = dict(video=open(document, 'rb'))
        return Message.from_api(api, **self._post('sendDocument', payload, files))

    def send_sticker(self, chat_id=None, sticker=None, reply_to_message_id=None, reply_markup=None):
        """
            Use this method to send .webp stickers. On success, the sent Message is returned.
        """
        payload = dict(chat_id=chat_id,
                       reply_to_message_id=reply_to_message_id,
                       reply_markup=reply_markup)
        files = dict(sticker=open(sticker, 'rb'))
        return Message.from_api(api, **self._post('sendSticker', payload, files))

    def send_video(self, chat_id, video, duration=None, caption=None, reply_to_message_id=None, reply_markup=None):
        """
            Use this method to send video files, Telegram clients support mp4 videos (other formats may be sent as
            Document). On success, the sent Message is returned. Bots can currently send video files of up to 50 MB
            in size, this limit may be changed in the future.
        """
        payload = dict(chat_id=chat_id,
                       duration=duration,
                       caption=caption,
                       reply_to_message_id=reply_to_message_id,
                       reply_markup=reply_markup)
        files = dict(video=open(video, 'rb'))
        return Message.from_api(api, **self._post('sendVideo', payload, files))

    def send_voice(self, chat_id, voice, duration=None, reply_to_message_id=None, reply_markup=None):
        """
            Use this method to send audio files, if you want Telegram clients to display the file as a playable voice
            message. For this to work, your audio must be in an .ogg file encoded with OPUS (other formats may be sent
            as Audio or Document). On success, the sent Message is returned. Bots can currently send voice messages of
            up to 50 MB in size, this limit may be changed in the future.
        """
        payload = dict(chat_id=chat_id,
                       duration=duration,
                       reply_to_message_id=reply_to_message_id,
                       reply_markup=reply_markup)
        files = dict(voice=open(voice, 'rb'))
        return Message.from_api(self, **self._post('sendVoice', payload, files))

    def send_location(self, loc, to, reply=None):
        """
            Use this method to send point on the map. On success, the sent Message is returned.
        """
        lat, lon = loc
        payload = dict(chat_id=to, reply_to_message_id=reply,
                       latitude=lat, longitude=lon)
        return Message.from_api(api, **self._get('sendLocation', payload))

    def send_chat_action(self, action, to):
        """
            Use this method when you need to tell the user that something is happening on the bot's side.
            The status is set for 5 seconds or less (when a message arrives from your bot,
            Telegram clients clear its typing status).
        """
        payload = dict(chat_id=to, action=action)
        return self._get('sendChatAction', payload)

    def get_user_profile_photos(self):
        """
            Use this method to get a list of profile pictures for a user. Returns a UserProfilePhotos object.
        """
        raise NotImplementedError()

    def get_updates(self, offset=None, limit=None, timeout=None):
        """
            Use this method to receive incoming updates using long polling (wiki).
            An Array of Update objects is returned.
        """
        payload = dict(offset=offset, limit=limit, timeout=timeout)
        return self._get('getUpdates', payload)

    def set_web_hook(self, url=None, certificate=None):
        """
            Use this method to specify a url and receive incoming updates via an outgoing webhook. Whenever there is an
            update for the bot, we will send an HTTPS POST request to the specified url, containing a JSON-serialized
            Update. In case of an unsuccessful request, we will give up after a reasonable amount of attempts.
        """
        payload = dict(url=url, certificate=certificate)
        return self._get('setWebHook', payload)

    def get_file(self, file_id):
        """
            Use this method to get basic info about a file and prepare it for downloading.
            For the moment, bots can download files of up to 20MB in size.
            On success, a File object is returned.
            The file can then be downloaded via the link https://api.telegram.org/file/bot<token>/<file_path>,
            where <file_path> is taken from the response. It is guaranteed that the link will be valid for at
            least 1 hour. When the link expires, a new one can be requested by calling get_file again.
        """
        return self._get('getFile', dict(file_id=file_id))
