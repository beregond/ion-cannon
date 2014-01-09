"""Models."""

import time
import json

from bson.objectid import ObjectId
from bson.errors import InvalidId

from . import get_storage


class Bullet(object):

    """Mapper for object in database."""

    __collection__ = 'Bullet'

    @classmethod
    def _get_collection(cls):
        return get_storage()['db'][cls.__collection__]

    @classmethod
    def _get_filesystem(cls):
        return get_storage()['fs']

    def __init__(self, **kwargs):
        # Fields.
        self.id = kwargs.get('_id')
        if self.id:
            self.id = str(self.id)
        self.headers = kwargs.get('headers')
        if self.headers and not isinstance(self.headers, dict):
            self.headers = json.loads(self.headers)
        self.uri = kwargs.get('uri')
        self.method = kwargs.get('method')
        self.content = kwargs.get('content')
        self.time = kwargs.get('time')
        self.file = kwargs.get('file')
        self.version = kwargs.get('version')

    def save(self):
        """Save model to database."""
        collection = self._get_collection()
        fs = self._get_filesystem()
        obj = {
            'headers': json.dumps(self.headers),
            'uri': self.uri,
            'method': self.method,
            'time': self.time,
            'version': self.version,
        }
        if self.content:
            file_obj = fs.put(self.content)
            obj['file'] = str(file_obj)
        result = collection.insert(obj)
        self.id = str(result)

    def delete(self):
        col = self._get_collection()
        fs = self._get_filesystem()
        col.remove({'_id': ObjectId(self.id)})
        if self.file:
            fs.delete(ObjectId(self.file))

    @classmethod
    def count(cls):
        """Count all available objects."""
        return cls._get_collection().count()

    @classmethod
    def all(cls):
        for item in cls._get_collection().find():
            yield cls(**item)

    @classmethod
    def remove_all(cls):
        """Remove all objects from database."""
        for bullet in cls.all():
            bullet.delete()

    @classmethod
    def get_by_id(cls, identity):
        col = cls._get_collection()

        try:
            identity = ObjectId(identity)
        except InvalidId:
            return None

        result = col.find_one({'_id': identity})
        return cls(**result) if result else None


class Clock(object):

    """Clock for fetch relative timestamps from given point."""

    @staticmethod
    def _get_timestamp():
        return int(round(time.time() * 1000))

    def __init__(self):
        self._zero = self._get_timestamp()

    def check(self):
        """Check time (in miliseconds).

        :return: Time in miliseconds.
        :rtype: int

        """
        return self._get_timestamp() - self._zero


class MainClock(object):

    """Singleton to keep reference to actually used Clock."""

    @classmethod
    def initialize(cls, clock):
        cls._clock = clock

    @classmethod
    def check(cls):
        try:
            return cls._clock.check()
        except AttributeError as e:
            raise RuntimeError("Main clock is wrongly or not initialized.")

    @classmethod
    def cleanup(cls):
        cls._clock = None
