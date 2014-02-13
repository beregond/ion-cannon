"""This module provides utilities to record and, send recorded requests."""

from functools import partial

from pymongo import MongoClient
from gridfs import GridFS

import settings

_KEY = 'storage'
_storage = {}


def _get_storage(cache):
    """Return dictionary with database and filesystem."""
    if cache.get(_KEY) is None:
        _set_storage(cache, )
    return cache.get(_KEY)


def _set_storage(cache, conf_key=None):
    if conf_key is None:
        conf_key = 'mongo'
    config = settings.config[conf_key]

    db = MongoClient(config['host'], int(config['port']))
    db = db[config['dbname']]
    fs = GridFS(db)
    storage = {'db': db, 'fs': fs}
    cache[_KEY] = storage

get_storage = partial(_get_storage, _storage)
set_storage = partial(_set_storage, _storage)
