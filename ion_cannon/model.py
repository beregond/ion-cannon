"""Models."""

from bson.objectid import ObjectId

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
        self.address = kwargs.get('address')
        self.method = kwargs.get('method')
        self.content = kwargs.get('content')
        self.time = kwargs.get('time')

    def save(self):
        """Save model to database."""
        collection = self._get_collection()
        fs = self._get_filesystem()
        file_obj = fs.put(self.content)
        obj = {
            'headers': self.headers,
            'address': self.address,
            'method': self.method,
            'time': self.time,
            'file': str(file_obj),
        }
        result = collection.insert(obj)
        self._id = str(result)

    def delete(self):
        col = self._get_collection()
        col.remove({'_id': ObjectId(self.id)})

    @classmethod
    def count(cls):
        """Count all available objects."""
        return cls._get_collection().count()

    @classmethod
    def all(cls):
        for item in cls._get_collection().find():
            yield Bullet(**item)

    @classmethod
    def remove_all(cls):
        """Remove all objects from database."""
        for bullet in cls.all():
            bullet.delete()
