"""Utilities for recording requests."""

from tornado.web import RequestHandler

from .model import Bullet, MainClock


class RecordHandler(RequestHandler):

    """Handler that records all incoming http request."""

    def head(self, *args, **kwargs):
        """Handle head request."""
        self.record(*args, **kwargs)

    def get(self, *args, **kwargs):
        """Handle get request."""
        self.record(*args, **kwargs)

    def post(self, *args, **kwargs):
        """Handle post request."""
        self.record(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Handle delete request."""
        self.record(*args, **kwargs)

    def patch(self, *args, **kwargs):
        """Handle patch request."""
        self.record(*args, **kwargs)

    def put(self, *args, **kwargs):
        """Handle put request."""
        self.record(*args, **kwargs)

    def options(self, *args, **kwargs):
        """Handle options request."""
        self.record(*args, **kwargs)

    def record(self, *args, **kwargs):
        """Record incoming http request."""
        obj = Bullet(
            uri=self.request.uri,
            time=MainClock.check(),
            headers=self.request.headers,
            method=self.request.method,
            version=self.request.version
        )
        obj.content = self.request.body if len(self.request.body) else None
        obj.save()


class MonitorHandler(RequestHandler):

    """Handler that just receives all incoming requests and do nothing more."""

    def head(self, *args, **kwargs):
        """Handle head request."""
        pass

    def get(self, *args, **kwargs):
        """Handle get request."""
        pass

    def post(self, *args, **kwargs):
        """Handle post request."""
        pass

    def delete(self, *args, **kwargs):
        """Handle delete request."""
        pass

    def patch(self, *args, **kwargs):
        """Handle patch request."""
        pass

    def put(self, *args, **kwargs):
        """Handle put request."""
        pass

    def options(self, *args, **kwargs):
        """Handle options request."""
        pass
