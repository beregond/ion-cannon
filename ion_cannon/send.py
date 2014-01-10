"""Utilities to send requests."""

from __future__ import print_function

import logging
from httplib import HTTPConnection

import settings
from .model import Bullet
from .error import NotFound


def sender(obj_id, httpclient=HTTPConnection):
    """Send http object with given id with use of given http client.

    Note: This should be done with use of
    ``tornado.httpclient.AsyncHTTPClient`` but it generates some problems (some
    of request are wrong), so for now request are synchronous.

    """
    logger = logging.getLogger('root')

    try:
        item = Bullet.get_by_id(obj_id)
    except NotFound:
        logger.error('Object with id "{}" was not found!'.format(obj_id))

    target = settings.config['target']

    method = item.method.upper()
    conn = httpclient(target)

    body = item.get_file().read() if item.has_file() else None

    conn.request(method, item.uri, body)
    res = conn.getresponse()
    logger.info('{} {} {} {} {}'.format(
        res.status, res.reason, item.id, method, item.uri))
