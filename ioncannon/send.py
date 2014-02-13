"""Utilities to send requests."""

from __future__ import print_function

import logging
from functools import partial

from tornado.httpclient import AsyncHTTPClient

import settings
from .model import Bullet
from .error import NotFound

LOGGER = logging.getLogger('root')


def response_handler(resp, oid, method, logger=LOGGER):
    """Handle response and log info about it.

    :param resp: HTTP response object.
    :param str oid: Object id.
    :param str method: Used method.

    """
    log = logger.error if resp.error else logger.info
    log('{} {} {} {} {}'.format(
        resp.code, resp.reason, oid, method, resp.effective_url))


def send(
        oid,
        httpclient=AsyncHTTPClient,
        target=settings.config['target'],
        handler=response_handler,
        logger=LOGGER):
    """Send http object with given id with use of given http client.

    :param str oid: Object id.
    :param httpclient: HTTP client to use.
    :param str target: Where to send request.
    :param function resp_handler: Response handler.
    :param object logger: Logger to use in case of error.
    :return: Future.

    """
    try:
        item = Bullet.get_by_id(oid)
    except NotFound:
        logger.error('Object with id "{}" was not found!'.format(oid))
        return

    url = target
    if url.endswith('/'):
        url = url[:-1]
    if not url.startswith('http://'):
        url = 'http://' + url
    url += item.uri

    client = httpclient()
    method = item.method.upper()
    body = item.get_file().read() if item.has_file() else None

    resp_handler = partial(handler, oid=oid, method=method)

    return client.fetch(
        url, resp_handler, method=method, body=body, headers=item.headers)
