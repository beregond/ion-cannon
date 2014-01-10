"""This module provides utilities to record and, send recorded requests."""

from functools import partial

from pymongo import MongoClient
from gridfs import GridFS

import settings

_storage = {}


def _get_storage(cache):
    """Return dictionary with database and filesystem.

    If ``settings.TEST`` is set to ``True`` it returns storage for test
    purposes.

    """
    if cache.get('storage') is None:
        if settings.TEST:
            config = settings.config['test_mongo']
        else:
            config = settings.config['mongo']

        db = MongoClient(config['host'], int(config['port']))
        db = db[config['dbname']]
        fs = GridFS(db)
        cache['storage'] = {'db': db, 'fs': fs}
    return cache['storage']

get_storage = partial(_get_storage, _storage)
