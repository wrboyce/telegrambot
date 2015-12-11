import unittest


from telegrambot.api import User


class TestUser(unittest.TestCase):
    def test_get_name_username(self):
        user = User(api=None)
        user.username = 'test'
        self.assertEqual(user.name, '@test')

    def test_get_name_fallback_full_name(self):
        user = User(api=None)
        user.first_name = 'Test'
        user.last_name = 'User'
        self.assertEqual(user.name, 'Test User')

    def test_get_name_fallback_first_name(self):
        user = User(api=None)
        user.first_name = 'Test'
        self.assertEqual(user.name, 'Test')
