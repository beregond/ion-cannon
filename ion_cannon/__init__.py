from functools import partial

from pymongo import MongoClient
from gridfs import GridFS

import settings

_storage = None


def _get_storage(cache):
    """Return dictionary with database and filesystem.

    If ``settings.TEST`` is set to ``True`` it returns storage for test
    purposes.

    """
    if cache is None:
        if settings.TEST:
            config = settings.config['test_mongo']
        else:
            config = settings.config['mongo']

        db = MongoClient(config['host'], int(config['port']))
        db = db[config['dbname']]
        fs = GridFS(db)
        cache = {'db': db, 'fs': fs}
    return cache

get_storage = partial(_get_storage, _storage)
