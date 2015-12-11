""" Copyright 2015 Will Boyce """
from __future__ import print_function, unicode_literals

import datetime
import os
import time

from telegrambot import api
from telegrambot.exceptions import TelegramBadRequestError
from telegrambot.logger import getLogger
from telegrambot.plugins.base import PluginRegistry
from telegrambot.version import __version__



class TelegramBot(api.TelegramAPIMixin):
    BASE_URL = 'https://api.telegram.org/bot'
    SLEEP_TIME = 0.5

    def __init__(self, cfg):
        super(TelegramBot, self).__init__(cfg)
        self.offset = 0
        self.username = self.get_me().username
        self.logger.info('@%s starting up (v%s)', self.username, __version__)
        self.stats = {'commands': 0, 'start_time': datetime.datetime.now()}
        self.version = __version__
        if self.cfg.core.media_dir is None:
            self.cfg.core.media_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'media')
        PluginRegistry.setup_plugins(self)

    @property
    def logger(self):
        return getLogger('telegrambot.bot')

    def get_updates(self):
        data = super(TelegramBot, self).get_updates(self.offset)
        if not data:
            return []
        self.offset = data[-1]['update_id'] + 1
        return data

    def process_updates(self):
        updates = self.get_updates()
        for payload in updates:
            self.logger.info('processing payload %s', payload)
            if 'message' in payload:
                msg = api.Message.from_api(api=self, **payload['message'])
                if msg.text and msg.text.startswith('/'):
                    args = msg.text.split(' ')
                    cmd = args.pop(0).lower().lstrip('/')
                    if cmd.endswith('@{}'.format(self.username).lower()):
                        cmd = cmd[:-(len(self.username) + 1)]
                    self.logger.debug('dispatching command %s(%s)', cmd, ' '.join(args))
                    self.dispatch_cmd(cmd, args, payload['message'])
                else:
                    self.dispatch_msg(payload['message'])
            else:
                self.dispatch(payload)

    def dispatch_cmd(self, cmd, args, msg):
        PluginRegistry.dispatch_cmd(self, cmd, args, msg)

    def dispatch_msg(self, msg):
        PluginRegistry.dispatch_msg(self, msg)

    def dispatch(self, payload):
        PluginRegistry.dispatch(self, payload)

    def handle_error(self, err, plugin=None, msg=None, silent=False):
        cause = plugin or self
        cause.logger.exception('[%s] %s', err.__class__.__name__, err)
        if silent or self.cfg.core.get('silent', False) or msg is None:
            return
        try:
            error_msg = "Woooah! Something went really wrong!\n\n[{}] {}".format(err.__class__.__name__, err)
            api.Message(api=cause, chat=msg.chat, text=error_msg, reply_to_message=msg).send()
        except TelegramBadRequestError:
            pass

    def loop(self):
        while True:
            try:
                self.process_updates()
                time.sleep(self.SLEEP_TIME)
            except KeyboardInterrupt:
                break
