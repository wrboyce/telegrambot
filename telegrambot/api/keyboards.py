""" Copyright 2015 Will Boyce """
from __future__ import print_function, unicode_literals

from telegrambot.api.base import APIObject


class ReplyKeyboardMarkup(APIObject):
    """
        This object represents a custom keyboard with reply options.

        keyboard	        Array of Array of String	Array of button rows, each represented by an Array of Strings
        resize_keyboard	    Boolean	                    (Optional) Requests clients to resize the keyboard vertically
                                                        for optimal fit (e.g., make the keyboard smaller if there are
                                                        just two rows of buttons). Defaults to false, in which case the
                                                        custom keyboard is always of the same height as the app's
                                                        standard keyboard.
        one_time_keyboard	Boolean	                    (Optional) Requests clients to hide the keyboard as soon as it's
                                                        been used. Defaults to false.
        selective	        Boolean	                    (Optional) Use this parameter if you want to show the keyboard
                                                        to specific users only. Targets:
                                                            1) users that are @mentioned in the text of the
                                                                Message object;
                                                            2) if the bot's message is a reply (has reply_to_message_id)
                                                                then sender of the original message.
    """
    _api_attrs = (
        ('keyboard', [[str]], TypeError),
        ('resize_keyboard', bool, False),
        ('one_time_keyboard', bool, False),
        ('selective', bool, False),
    )


class ReplyKeyboardHide(APIObject):
    """
        Upon receiving a message with this object, Telegram clients will hide the current custom keyboard and display
        the default letter-keyboard. By default, custom keyboards are displayed until a new keyboard is sent by a bot.
        An exception is made for one-time keyboards that are hidden immediately after the user presses a button.

        hide_keyboard	True	    Requests clients to hide the custom keyboard
        selective	    Boolean	    (Optional) Use this parameter if you want to hide keyboard for specific users only.
                                    Targets:
                                        1) users that are @mentioned in the text of the Message object;
                                        2) if the bot's message is a reply (has reply_to_message_id),
                                            sender of the original message.
    """
    _api_attrs = (
        ('hide_keyboard', bool, True),
        ('selective', bool, False),
    )


class ForceReply(APIObject):
    """
        Upon receiving a message with this object, Telegram clients will display a reply interface to the user
        (act as if the user has selected the bot's message and tapped 'Reply').

        force_reply	    True	    Shows reply interface to the user, as if they manually selected the bot's message
                                    and tapped 'Reply'
        selective	    Boolean	    (Optional) Use this parameter if you want to force reply from specific users only.
                                    Targets:
                                        1) users that are @mentioned in the text of the Message object;
                                        2) if the bot's message is a reply (has reply_to_message_id),
                                            sender of the original message.
    """
    _api_attrs = (
        ('force_reply', bool, True),
        ('selective', bool, False),
    )