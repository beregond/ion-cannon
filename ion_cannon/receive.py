"""Utilities for recording requests."""

from tornado.gen import coroutine
from tornado.web import RequestHandler

from .model import Bullet, Clock
from .send import send


@coroutine
def handle(self):
    """Record incoming http request."""
    yield next(self.record())


class RecordHandler(RequestHandler):

    """Handler that records all incoming http request."""

    get = handle
    post = handle
    head = handle
    options = handle
    delete = handle
    put = handle
    patch = handle

    def initialize(self, tunnel=False):
        """Initialize handler."""
        self.tunnel = tunnel

    def _handler(self, request, *args, **kwargs):
        for header, value in request.headers.items():
            self.set_header(header, value)
        self.write(request.body)

    def record(self):
        """Record request."""
        obj = Bullet(
            uri=self.request.uri,
            time=Clock.check(),
            headers=self.request.headers,
            method=self.request.method,
        )
        obj.content = self.request.body if len(self.request.body) else None
        obj.save()

        if self.tunnel:
            yield send(obj.id, handler=self._handler)
        self.finish()


def empty_func(self):
    """Handle request."""
    pass


class MonitorHandler(RequestHandler):

    """Handler that just receives all incoming requests and do nothing more."""

    head = empty_func
    get = empty_func
    post = empty_func
    delete = empty_func
    patch = empty_func
    put = empty_func
    options = empty_func
