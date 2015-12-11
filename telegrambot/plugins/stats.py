""" Copyright 2015 Will Boyce """
from __future__ import print_function, unicode_literals

import datetime
import itertools

import humanize

from telegrambot.plugins.base import BasePlugin
from telegrambot.util import humanize_int


class Stats(BasePlugin):
    commands = {
        'stats': 'get_stats',
        'plugins': 'get_plugins',
        'commands': 'get_commands',
    }

    def get_stats(self, _args, msg):
        stats_msg = "{bot_name} running telegrambot v{version} <https://www.github.com/wrboyce/telegrambot>.\nStarted {uptime} with {n_plugins} plugins; processed {n_commands} commands.".format(**{
            'bot_name': self.bot.username,
            'version': self.bot.version,
            'n_commands': humanize_int(self.bot.stats['commands']),
            'uptime': humanize.naturaltime(datetime.datetime.now() - self.bot.stats['start_time']),
            'n_plugins': len(self.bot.plugins),
        })
        msg.reply(stats_msg, hide_urls=True)

    def get_plugins(self, _args, msg):
        n_commands = len([cmd for cmd in itertools.chain(*[p.commands.iterkeys() for p in self.bot.plugins])])
        reply = "{n_plugins} plugins loaded providing {n_commands} commands.\n\nPlugins: {plugins_list}"
        reply = reply.format(**{
            'n_plugins': len(self.bot.plugins),
            'n_commands': humanize_int(n_commands),
            'plugins_list': ', '.join(sorted(p.__class__.__name__ for p in self.bot.plugins)),
        })
        msg.reply(reply)

    def get_commands(self, _args, msg):
        commands = sorted(
                '/{}'.format(cmd) for cmd in itertools.chain(*[p.commands.iterkeys() for p in self.bot.plugins]))
        reply = "{n_plugins} plugins loaded providing {n_commands} commands.\n\nCommands: {commands_list}"
        reply = reply.format(**{
            'n_plugins': len(self.bot.plugins),
            'n_commands': humanize_int(len(commands)),
            'commands_list': ', '.join(commands),
        })
        msg.reply(reply)
