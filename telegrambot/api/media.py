""" Copyright 2015 Will Boyce """
from __future__ import print_function, unicode_literals

from telegrambot.api.base import APIObject


class Audio(APIObject):
    """
        This object represents an audio file to be treated as music by the Telegram clients.

        file_id	        str 	Unique identifier for this file
        duration	    int     Duration of the audio in seconds as defined by sender
        performer	    str 	(Optional) Performer of the audio as defined by sender or by audio tags
        title	        str 	(Optional) Title of the audio as defined by sender or by audio tags
        mime_type	    str 	(Optional) MIME type of the file as defined by sender
        file_size	    int  	(Optional) File size
    """
    _api_attrs = (
        ('file_id', str, TypeError),
        ('duration', int, TypeError),
        ('performer', str, None),
        ('title', str, None),
        ('mime_type', str, None),
        ('file_size', int, None),
    )


class Contact(APIObject):
    """
        This object represents a phone contact.

        phone_number	str 	Contact's phone number
        first_name	    str 	Contact's first name
        last_name	    str 	(Optional) Contact's last name
        user_id	        int 	(Optional) Contact's user identifier in Telegram
    """
    _api_attrs = (
        ('phone_number', str, TypeError),
        ('first_name', str, TypeError),
        ('last_name', str, None),
        ('user_id', int, None),
    )


class PhotoSize(APIObject):
    """ This object represents one size of a photo or a file / sticker thumbnail.

        file_id	    str 	Unique identifier for this file
        width	    int 	Photo width
        height	    int 	Photo height
        file_size	int 	(Optional) File size
    """
    _api_attrs = (
        ('file_id', str, TypeError),
        ('width', int, TypeError),
        ('height', int, TypeError),
        ('file_size', int, None),
    )


class Document(APIObject):
    """
        This object represents a general file (as opposed to photos, voice messages and audio files).

        file_id	    str 	    Unique file identifier
        thumb	    PhotoSize	(Optional) Document thumbnail as defined by sender
        file_name	str 	    (Optional) Original filename as defined by sender
        mime_type	str 	    (Optional) MIME type of the file as defined by sender
        file_size	int 	    (Optional) File size
    """
    _api_attrs = (
        ('file_id', str, TypeError),
        ('thumb', PhotoSize, None),
        ('file_name', str, None),
        ('mime_type', str, None),
        ('file_size', int, None),
    )


class File(APIObject):
    """
        This object represents a file ready to be downloaded. The file can be downloaded via the link
        https://api.telegram.org/file/bot<token>/<file_path>. It is guaranteed that the link will be valid for at least
        1 hour. When the link expires, a new one can be requested by calling getFile.

        file_id	    String	Unique identifier for this file
        file_size	int 	(Optional) File size, if known
        file_path	str 	(Optional) File path.
                                Use https://api.telegram.org/file/bot<token>/<file_path> to get the file.
    """
    _api_attrs = (
        ('file_id', str, TypeError),
        ('file_size', int, None),
        ('file_path', str, None)
    )


class Location(APIObject):
    """
        This object represents a point on the map.

        longitude	Float	Longitude as defined by sender
        latitude	Float	Latitude as defined by sender
    """
    _api_attrs = (
        ('longitude', float, None),
        ('latitude', float, None),
    )


class Sticker(APIObject):
    """
        This object represents a sticker.

        file_id	    str 	    Unique identifier for this file
        width	    int 	    Sticker width
        height	    int 	    Sticker height
        thumb	    PhotoSize	(Optional) Sticker thumbnail in .webp or .jpg format
        file_size	int 	    (Optional) File size
    """
    _api_attrs = (
        ('file_id', str, TypeError),
        ('width', int, TypeError),
        ('height', int, TypeError),
        ('thumb', PhotoSize, None),
        ('file_size', int, None),
    )


class Video(APIObject):
    """
        This object represents a video file.

        file_id	    str 	    Unique identifier for this file
        width	    int 	    Video width as defined by sender
        height	    int 	    Video height as defined by sender
        duration	int 	    Duration of the video in seconds as defined by sender
        thumb	    PhotoSize	(Optional) Video thumbnail
        mime_type	str 	    (Optional) Mime type of a file as defined by sender
        file_size	int     	(Optional) File size
    """
    _api_attrs = (
        ('file_id', str, TypeError),
        ('width', int, TypeError),
        ('height', int, TypeError),
        ('duration', int, TypeError),
        ('thumb', PhotoSize, None),
        ('mime_type', str, None),
        ('file_size', int, None),
    )


class Voice(APIObject):
    """
        This object represents a voice note.

        file_id	    str 	Unique identifier for this file
        duration	int 	Duration of the audio in seconds as defined by sender
        mime_type	str 	(Optional) MIME type of the file as defined by sender
        file_size	int 	(Optional) File size
    """
    _api_attrs = (
        ('file_id', str, TypeError),
        ('duration', int, TypeError),
        ('mime_type', str, None),
        ('file_size', int, None),
    )
