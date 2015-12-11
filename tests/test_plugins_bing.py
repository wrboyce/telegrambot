import unittest

from mock import MagicMock

from telegrambot import api
from telegrambot.plugins.bing import BingSearch


class TestBing(unittest.TestCase):
    def test_no_key(self):
        bot = MagicMock()
        bot.cfg.bing.key = None
        bing_plugin = BingSearch(bot)
        bing_plugin.send_chat_action = MagicMock()
        msg = api.Message.from_api(api=bot, **{
            'text': '/get image',
            'message_id': 1,
            'date': 0,
            'chat': {'id': 1, 'first_name': 'test', 'type': 'private'},
        })
        bing_plugin.get_image(['image'], msg)
        bot.send_message.assert_called_with(
                chat_id=1,
                disable_web_page_preview=False,
                reply_to_message_id=1,
                text=u'No results found :(')

    def test_no_results(self):
        bot = MagicMock()
        bot.cfg.bing.key = 'test-key'
        bing_plugin = BingSearch(bot)
        bing_plugin._search = MagicMock(return_value=[])
        bing_plugin.send_chat_action = MagicMock()
        msg = api.Message.from_api(api=bot, **{
            'text': '/get image',
            'message_id': 1,
            'date': 0,
            'chat': {'id': 1, 'first_name': 'test', 'type': 'private'},
        })
        bing_plugin.get_image(['image'], msg)
        bot.send_message.assert_called_with(
            chat_id=1,
            disable_web_page_preview=False,
            reply_to_message_id=1,
            text=u'No results found :(')