"""Test send functions."""

from tornado.web import Future

from . import switch_to_test_db
from ..send import send, response_handler
from ..model import Bullet


class DummyResponse(object):

    """Dummy response."""

    def __init__(self, body):
        self.error = False
        self.body = body
        self.headers = {'version': '1.0'}


class DummyLogger(object):

    """Logger for test purposes."""

    def __init__(self):
        self.error_msg = False
        self.info_msg = False

    def error(self, msg):
        self.error_msg = msg

    def info(self, msg):
        self.info_msg = msg


class DummyHTTPClient(object):

    """HTTP like client for test purposes."""

    @classmethod
    def reset(cls):
        cls.url = None
        cls.handler = None
        cls.kwargs = {}

    @classmethod
    def fetch(cls, url, handler, **kwargs):
        cls.url = url
        cls.handler = handler
        cls.kwargs = kwargs
        fut = Future()
        fut.set_result('some result')

        resp = DummyResponse('some body')
        handler(resp)

        return fut


def test_response_handler():
    resp = type('tmp', (), {
        "code": "200",
        "reason": "OK",
        "error": False,
        "effective_url": "http://url.com/",
    })

    logger = DummyLogger()

    response_handler(resp, '123', 'GET', logger)

    assert logger.error_msg is False
    assert logger.info_msg == '200 OK 123 GET http://url.com/'


def test_response_handler_with_error():
    resp = type('tmp', (), {
        "code": "500",
        "reason": "Error",
        "error": True,
        "effective_url": "http://url.com/",
    })

    logger = DummyLogger()

    response_handler(resp, '321', 'POST', logger)

    assert logger.info_msg is False
    assert logger.error_msg == '500 Error 321 POST http://url.com/'


def test_send_with_not_existent_object():
    switch_to_test_db()
    Bullet.remove_all()
    assert Bullet.count() == 0

    logger = DummyLogger()
    handler = lambda *args, **kwargs: None
    handler()

    send(
        'some_oid', httpclient=DummyHTTPClient, target="http://someurl/",
        handler=handler, logger=logger)

    assert logger.error_msg == 'Object with id "some_oid" was not found!'


def test_send():
    switch_to_test_db()
    Bullet.remove_all()
    assert Bullet.count() == 0

    x = Bullet()
    x.headers = {"some_header": "some_value"}
    x.uri = '/other'
    x.method = 'post'
    x.content = 'other content'
    x.time = 10
    x.save()

    logger = DummyLogger()
    handler = lambda *args, **kwargs: None
    handler()

    client = DummyHTTPClient

    for target in ['http://someurl/', 'http://someurl', 'someurl', 'someurl/']:
        client.reset()

        send(
            x.id, httpclient=client, target=target,
            handler=handler, logger=logger)

        assert logger.info_msg is False
        assert logger.error_msg is False
        assert client.url == 'http://someurl/other'
        assert client.kwargs['headers'] == x.headers
        assert client.kwargs['method'] == 'POST'
        assert client.kwargs['body'] == 'other content'
