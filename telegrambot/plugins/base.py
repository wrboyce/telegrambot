""" Copyright 2015 Will Boyce """
from __future__ import print_function, unicode_literals

import threading
import time

from telegrambot import api
from telegrambot.logger import getLogger


logger = getLogger('telegrambot.plugins')


class PluginSet(set):
    """ I don't like this class. """
    def __init__(self, *args, **kwargs):
        self.classes = set()
        super(PluginSet, self).__init__(*args, **kwargs)

    def add(self, item):
        if item.__name__ in self.classes:
            return
        self.classes.add(item.__name__)
        super(PluginSet, self).add(item)


class PluginRegistry(type):
    _plugins = PluginSet()

    def __init__(cls, name, bases, attrs):
        if not attrs.pop('abstract', False):
            PluginRegistry._plugins.add(cls)
        super(PluginRegistry, cls).__init__(name, bases, attrs)

    @classmethod
    def setup_plugins(mcs, bot):
        bot.plugins = set()
        for PluginClass in mcs._plugins:
            if bot.cfg.core.plugins is None or PluginClass.__name__ in bot.cfg.core.plugins:
                logger.debug("adding '%s' plugin instance", PluginClass.__name__)
                bot.plugins.add(PluginClass(bot))
            else:
                logger.debug("skipping plugin '%s'", PluginClass.__name__)

    @classmethod
    def dispatch_cmd(mcs, bot, cmd, args, msg_payload):
        for plugin in bot.plugins:
            msg = api.Message.from_api(api=plugin, **msg_payload)
            mcs._dispatch(bot=bot, target=plugin, msg=msg, args=(cmd, args, msg))

    @classmethod
    def dispatch_msg(mcs, bot, msg_payload):
        for plugin in bot.plugins:
            if hasattr(plugin, 'handle_msg'):
                msg = api.Message.from_api(api=plugin, **msg_payload)
                mcs._dispatch(bot=bot, target=(plugin, 'handle_msg'), msg=msg, args=[msg])

    @classmethod
    def dispatch(mcs, bot, payload):
        for plugin in bot.plugins:
            if hasattr(plugin, 'handle_payload'):
                mcs._dispatch(bot=bot, target=(plugin, 'handle_update'), args=[payload])

    @classmethod
    def _dispatch(mcs, bot, target, msg=None, args=None):
        if args is None:
            args = [msg]
        PluginThread(bot=bot, msg=msg, target=target, args=args).start()


class PluginThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        self.bot = kwargs.pop('bot')
        self.msg = kwargs.pop('msg')
        target = kwargs.get('target')
        if isinstance(target, (list, tuple)):
            self.plugin = target[0]
            self.target = getattr(target[0], target[1])
            kwargs['target'] = self.target
        else:
            self.plugin = target
            self.target = target
        super(PluginThread, self).__init__(*args, **kwargs)

    def run(self):
        try:
            super(PluginThread, self).run()
        except Exception, err:
            reply_error = self.target is self.plugin  # only reply with errors to commands?
            self.bot.handle_error(err, plugin=self.plugin, msg=self.msg, silent=not reply_error)


class BasePlugin(api.TelegramAPIMixin):
    abstract = True
    commands = {}
    __metaclass__ = PluginRegistry

    def __init__(self, bot):
        self.bot = bot
        super(BasePlugin, self).__init__(bot.cfg)

    def __call__(self, cmd, args, msg):
        if not hasattr(self, 'commands'):
            return
        if cmd not in self.commands:
            return
        if not hasattr(self, self.commands[cmd]):
            return
        self.bot.stats['commands'] += 1
        self.logger.info("responding to command %s(%s)", cmd, ', '.join(args))
        handler = getattr(self, self.commands[cmd])
        handler(args, msg)

    @property
    def logger(self):
        class_path = '.'.join([self.__class__.__module__, self.__class__.__name__])
        if not class_path.startswith('telegrambot.plugins'):
            class_path = 'telegrambot.plugins.{}'.format(class_path)
        return getLogger(class_path)


class Debug(BasePlugin):
    commands = {'crash': 'crash',
                'hang': 'hang'}

    def crash(self, _args, _msg):  # pylint: disable=no-self-use, unused-argument
        return 1 / 0  # BOOM!

    def hang(self, _args, _msg):
        time.sleep(60)
