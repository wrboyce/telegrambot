from __future__ import print_function, unicode_literals

import os

import requests

from telegrambot import util
from telegrambot.plugins.base import BasePlugin


class XKCD(BasePlugin):
    commands = {'xkcd': 'handle_cmd'}

    def handle_cmd(self, args, msg):
        path = ''
        if args:
            try:
                id = int(args[0])
                path = '/{}/'.format(id)
            except (IndexError, ValueError):
                pass
        url = 'http://xkcd.com/{}info.0.json'.format(path)
        data = requests.get(url).json()
        try:
            img_fn = util.download_tmp_file(data['img'])
            self.send_photo(msg.chat.id, img_fn, caption=data['alt'], reply_to_message_id=msg.message_id)
        finally:
            os.unlink(img_fn)

