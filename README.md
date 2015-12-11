<strike>Disclaimer</strike> README
==================================

[![Build Status](https://img.shields.io/travis/wrboyce/telegrambot.svg)](https://travis-ci.org/wrboyce/telegrambot)
[![Coverage Status](https://img.shields.io/codecov/c/github/wrboyce/telegrambot.svg)](https://codecov.io/github/wrboyce/telegrambot)
[![Code Quality](https://img.shields.io/codacy/9f4cdfa263b149c0853fbb3a1ff22e4a.svg)](https://www.codacy.com/app/wrboyce/telegrambot)
[![Current Version](https://img.shields.io/pypi/v/telegrambot.svg)](https://pypi.python.org/pypi/telegrambot)
[![Python Versions](https://img.shields.io/pypi/pyversions/telegrambot.svg)](https://pypi.python.org/pypi/telegrambot)

Despite this code having been in production in quite a heavy use environment
for a good few months, I really wouldn't class it as an example of great code.

It would be fair to say I got sidetracked, and decided to see how much I could
abuse certain aspects of Python (such as metaclasses/class creation).

You have been warned!

With that out of the way, `telegrambot` is pretty easy to get up and running.

    % pip install telegrambot
    % cat mybot.cfg
    [core]
    bot_id = <telegram_bot_id>
    token = <telegram_bot_token>
    [bing]
    key = <bing_api_key>
    % telegrambot mybot.cfg


As it stands the framework exposes three commands; `/crash` and `/hang` were
used to test error handling and threading during development whereas `/get`
is a bring-your-own-api-key bing image searcher.

Adding plugins aims to be really easy, just create a namespace package under
`telegrambot.plugins` and subclass `telegrambot.plugins.base.BasePlugin`
(now that I think about it, the namespace package may not be necessary - I will
have to re-think my motivation on that one).

Example Plugin
--------------

```python
from telegrambot.plugins.base import BasePlugin

# due to annoying limitations class names must be unique
class HelloWorld(BasePlugin):
    # register /hello command to 'hello_handler' method
    commands {'hello': 'hello_handler'}

    def hello_handler(self, args, msg):
        # `args` is a list of the arguments after the command:
        # '/hello world' -> args=['world']
        # `msg` is a dictionary representing the Telegram `Message` object
        # see TelegramAPIMixin for available Telegram API functions
        self.send_message('Hello, {}'.(' '.join(args)),
                          msg['chat']['id'],
                          reply=msg['message_id'])
```
