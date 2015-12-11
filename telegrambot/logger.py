""" Copyright 2015 Will Boyce """
from __future__ import print_function, unicode_literals

import logging
from logging import getLogger


logger = getLogger('telegrambot')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(name)s %(message)s'))
logger.addHandler(handler)