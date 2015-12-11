""" Copyright 2015 Will Boyce """
from __future__ import print_function, unicode_literals

import os
import tempfile

import humanize
import requests


def is_int(i):
    try:
        int(i)
    except ValueError:
        return False
    return True

def humanize_int(i):
    if is_int(i):
        i = humanize.apnumber(i)
    if is_int(i):
        i = humanize.intword(i)
    if is_int(i):
        i = humanize.intcomma(i)
    return i

def is_image(filename):
    ext = os.path.splitext(filename)[1]
    return ext.lower() in ('.jpg', '.jpeg', '.gif', '.png', '.tif', '.bmp')

def download_tmp_file(url):
    filename = url.split('?', 1)[0]
    _, img_fn = tempfile.mkstemp(suffix=os.path.splitext(filename)[1])
    resp = requests.get(url)
    with open(img_fn, 'wb') as img_fh:
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                img_fh.write(chunk)
                img_fh.flush()
    return img_fn