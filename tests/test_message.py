import unittest

from mock import Mock, MagicMock

from telegrambot import api


class TestMessage(unittest.TestCase):
    def test_init_with_objects(self):
        bot = MagicMock()
        chat = api.Chat.from_api(api=bot, **{'id': 1, 'type': 'private'})
        msg = api.Message(api=bot, chat=chat, text='Testing...')
        self.assertEqual(msg.chat_id, chat.id)
        msg.message_id = 100
        reply = api.Message(api=bot, chat=chat, text='It worked!', reply_to_message=msg)
        self.assertEqual(reply.reply_to_message_id, msg.message_id)

    def test_send(self):
        bot = MagicMock()
        api.Message(api=bot, chat=1, text='Hello, World!').send()
        bot.send_message.assert_called_with(
            text='Hello, World!',
            chat_id=1,
        )

    def test_forward_same_chat(self):
        bot = Mock()
        msg = api.Message(api=bot, chat=1)
        msg.message_id = 3
        msg.forward()
        bot.forward_message.assert_called_with(
            chat_id=1,
            from_chat_id=1,
            message_id=3,
        )

    def test_forward_other_chat(self):
        bot = Mock()
        msg = api.Message(api=bot, chat=1)
        msg.message_id = 3
        msg.forward(chat_id=2)
        bot.forward_message.assert_called_with(
            chat_id=2,
            from_chat_id=1,
            message_id=3,
        )


# TODO: test `reply`
class XXX(object):
    def test_reply(self):
        bot = MagicMock()
        msg_payload = {
            'message_id': 1,
            'date': 0,
            'text': 'TEST',
            'from': {
                'username': 'test',
                'first_name': 'Test',
                'last_name': 'User',
                'id': 2
            },
            'chat': {
                'username': 'test',
                'first_name': 'Test',
                'last_name': 'User',
                'type': 'private',
                'id': 3
            }
        }
        msg = api.Message.from_api(api=bot, **msg_payload)
        msg.reply(text='Hello, @test!')
        bot.send_message.assert_called_with(
            text='Hello, @test!',
            reply_to_message_id=1,
            chat_id=3,
            disable_web_page_preview=False
        )

    def test_forward(self):
        bot = MagicMock()
        msg_payload = {
            'message_id': 1,
            'date': 0,
            'text': 'TEST',
            'from': {
                'username': 'test',
                'first_name': 'Test',
                'last_name': 'User',
                'id': 2
            },
            'chat': {
                'username': 'test',
                'first_name': 'Test',
                'last_name': 'User',
                'type': 'private',
                'id': 3
            }
        }
        msg = api.Message.from_api(api=bot, **msg_payload)
        msg.forward()
        bot.forward_message.assert_called_with(
            chat_id=msg.chat_id,
            from_chat_id=msg.chat_id,
            message_id=msg.message_id
        )