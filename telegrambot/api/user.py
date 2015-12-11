""" Copyright 2015 Will Boyce """
from __future__ import print_function, unicode_literals


from telegrambot.api.base import APIObject
from telegrambot.api.media import PhotoSize


class User(APIObject):
    """ This object represents a Telegram user or bot.

        id          int     Unique identifier for this user or bot
        first_name  str     User's or bot's first name
        last_name   str     (Optional) User's or bot's last name
        username    str     (Optional) User's or bot's username
    """
    _api_attrs = (
        ('id', int, TypeError),
        ('first_name', str, TypeError),
        ('last_name', str, None),
        ('username', str, None),
    )

    @property
    def name(self):
        if self.username:
            return '@{}'.format(self.username)
        return '{} {}'.format(self.first_name, self.last_name).strip()


class UserProfilePhotos(APIObject):
    """
        This object represent a user's profile pictures.

        total_count	int 	                        Total number of profile pictures the target user has
        photos	    Array of Array of PhotoSize	    Requested profile pictures (in up to 4 sizes each)
    """
    _api_attrs = (
        ('total_count', int, TypeError),
        ('photos', [[PhotoSize]], TypeError),
    )