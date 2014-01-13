"""Utilities to send requests."""

from __future__ import print_function

import logging
from functools import partial

from tornado.httpclient import AsyncHTTPClient

import settings
from .model import Bullet
from .error import NotFound

LOGGER = logging.getLogger('root')


def resp_handler(resp, oid, method, logger=LOGGER):
    """Handle response and log info about it.

    :param resp: HTTP response object.
    :param str oid: Object id.
    :param str method: Used method.

    """
    logger = logging.getLogger('root')
    log = logger.error if resp.error else logger.info
    log('{} {} {} {} {}'.format(
        resp.code, resp.reason, oid, method, resp.effective_url))


def sender(
        oid,
        httpclient=AsyncHTTPClient,
        target=settings.config['target'],
        logger=LOGGER):
    """Send http object with given id with use of given http client.

    :param str oid: Object id.
    :param httpclient: HTTP client to use.
    :param str target: Where to send request.

    """
    try:
        item = Bullet.get_by_id(oid)
    except NotFound:
        logger.error('Object with id "{}" was not found!'.format(oid))
        return

    target = settings.config['target']
    if target.endswith('/'):
        target = target[:-1]
    if not target.startswith('http://'):
        target = 'http://' + target
    target += item.uri

    client = httpclient()
    method = item.method.upper()
    body = item.get_file().read() if item.has_file() else None

    handler = partial(resp_handler, oid=oid, method=method)

    client.fetch(
        target, handler, method=method, body=body, headers=item.headers)
