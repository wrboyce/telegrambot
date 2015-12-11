""" Copyright 2015 Will Boyce """
from __future__ import print_function, unicode_literals

from telegrambot.api.base import APIObject


class Chat(APIObject):
    """ This object represents a chat.

        id	        int 	Unique identifier for this chat, not exceeding 1e13 by absolute value
        type	    str 	(Type of chat, can be either "private", "group", "supergroup" or "channel"
        title	    str 	(Optional) Title, for channels and group chats
        username	str 	(Optional) Username, for private chats and channels if available
        first_name	str 	(Optional) First name of the other party in a private chat
        last_name	str 	(Optional) Last name of the other party in a private chat
    """
    _api_attrs = (
        ('id', int, TypeError),
        ('type', str, TypeError),
        ('title', str, None),
        ('username', str, None),
        ('first_name', str, None),
        ('last_name', str, None),
    )