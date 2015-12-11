import json
import unittest

import httpretty
from mock import Mock

from telegrambot import api
from telegrambot.exceptions import TelegramBadRequestError


class DummyAPI(api.TelegramAPIMixin):
    def __init__(self):
        return


class TestAPIMixin(unittest.TestCase):
    def test_logger_name(self):
        api = DummyAPI()
        self.assertEqual(api.logger.name, 'telegrambot.tests.test_api.DummyAPI')


class TestAPIGetPost(unittest.TestCase):
    def setUp(self):
        super(TestAPIGetPost, self).setUp()
        cfg = Mock()
        cfg.core.bot_id = 'bot-id'
        cfg.core.token = 'token'
        self.bot = api.TelegramAPIMixin(cfg)

    @httpretty.activate
    def test_get_not_ok(self):
        payload = {'ok': False, 'error_code': 500, 'description': 'test'}
        url = '{}/errorTest'.format(self.bot.base_url)
        httpretty.register_uri(httpretty.GET, url,
                               body=json.dumps(payload))
        self.assertRaises(TelegramBadRequestError, self.bot._get, 'errorTest')

    @httpretty.activate
    def test_get_ok(self):
        payload = {'ok': True, 'result': None}
        url = '{}/okTest'.format(self.bot.base_url)
        httpretty.register_uri(httpretty.GET, url,
                               body=json.dumps(payload))
        self.assertEqual(self.bot._get('okTest'), None)

    @httpretty.activate
    def test_post_not_ok(self):
        payload = {'ok': False, 'error_code': 500, 'description': 'test'}
        url = '{}/errorTest'.format(self.bot.base_url)
        httpretty.register_uri(httpretty.POST, url,
                               body=json.dumps(payload))
        self.assertRaises(TelegramBadRequestError, self.bot._post, 'errorTest')

    @httpretty.activate
    def test_post_ok(self):
        payload = {'ok': True, 'result': None}
        url = '{}/okTest'.format(self.bot.base_url)
        httpretty.register_uri(httpretty.POST, url,
                               body=json.dumps(payload))
        self.assertEqual(self.bot._post('okTest'), None)


class TestAPIHelpers(TestAPIGetPost):
    @httpretty.activate
    def test_get_me_ok(self):
        user_payload = {'id': 1, 'first_name': 'Test', 'last_name': 'User', 'username': 'test'}
        payload = {'ok': True, 'result': user_payload}
        url = '{}/getMe'.format(self.bot.base_url)
        httpretty.register_uri(httpretty.GET, url,
                               body=json.dumps(payload))
        self.assertIsInstance(self.bot.get_me(), api.User)
