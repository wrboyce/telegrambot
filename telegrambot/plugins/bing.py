""" Copyright 2015 Will Boyce """
from __future__ import print_function, unicode_literals

import os
import random
import tempfile

import requests

from telegrambot import util
from telegrambot.plugins.base import BasePlugin


class BingSearch(BasePlugin):
    locale = 'en-GB'

    commands = {
        'get': 'get_image',
    }

    class SearchTypes(type):
        images = 'Image'

    def get_image(self, args, msg):
        self.send_chat_action('typing', to=msg.chat.id)
        query = ' '.join(args)
        result = self._get_random_result(query, search_type=self.SearchTypes.images)
        if result is None:
            return msg.reply('No results found :(')
        self.send_chat_action('upload_photo', to=msg.chat.id)
        img_url = result['MediaUrl']
        try:
            img_fn = util.download_tmp_file(img_url)
            self.send_photo(msg.chat.id, img_fn, reply_to_message_id=msg.message_id)
        finally:
            os.unlink(img_fn)

    def _get_random_result(self, *args, **kwargs):
        try:
            return random.choice(self._search(*args, **kwargs))
        except IndexError:
            pass

    def _search(self, query, search_type=None):
        if not self.bot.cfg.bing.key:
            return []
        if search_type is None:
            raise NotImplementedError()
        url = 'https://api.datamarket.azure.com/Bing/Search/v1/{}'.format(search_type)
        params = {
            'Query': query,
            'Adult': 'Off',
            '$format': 'json',
        }
        if self.locale is not None:
            params['Market'] = self.locale
        params = {k: "'{}'".format(v) if not k.startswith('$') else v for k, v in params.iteritems()}
        data = requests.get(url, params=params, auth=(self.bot.cfg.bing.key, self.bot.cfg.bing.key)).json()['d']
        return data['results']
