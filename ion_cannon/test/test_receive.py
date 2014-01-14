"""Test receive handlers."""

from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from . import switch_to_test_db
from ..model import Bullet
from ..receive import MonitorHandler, RecordHandler

METHODS = ['get', 'post', 'head', 'options', 'delete', 'patch', 'put']
METHODS_WITH_BODY = ['post', 'patch', 'put']


def _iterate_methods():
    for method in METHODS:
        body = 'body' if method in METHODS_WITH_BODY else None
        yield method, body


class TestMonitorHandler(AsyncHTTPTestCase):

    def get_app(self):
        return Application([(r'/.*', MonitorHandler)])

    def test_http_fetch(self):
        switch_to_test_db()
        Bullet.remove_all()
        for method, body in _iterate_methods():
            response = self.fetch('/', method=method.upper(), body=body)
            assert response.code == 200
            assert Bullet.count() == 0


class TestRecordHandler(AsyncHTTPTestCase):

    def get_app(self):
        return Application([(r'/.*', RecordHandler)])

    def test_http_fetch(self):
        switch_to_test_db()
        for method, body in _iterate_methods():
            Bullet.remove_all()
            assert Bullet.count() == 0
            response = self.fetch('/', method=method.upper(), body=body)
            assert response.code == 200
            assert Bullet.count() == 1
            it = Bullet.all()
            bullet = it.next()
            if bullet.has_file():
                assert bullet.get_file().read() == body
