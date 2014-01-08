"""Utilities for tests."""

from pymongo import MongoClient
from gridfs import GridFS

import settings


def get_storage():
    """Return dictionary with database and filesystem for test purposes."""
    config = settings['test_mongo']
    db = MongoClient(config['host'], config['port'])
    import pdb
    pdb.set_trace()
    db = db[config['dbname']]
    fs = GridFS(db)
    return {'db': db, 'fs': fs}
