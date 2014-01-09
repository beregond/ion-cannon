"""Cannon to record and later send recorded http request to target url."""

import sys

import tornado.ioloop
import tornado.web

from ion_cannon.record import RecordHandler
from ion_cannon.model import Bullet, MainClock, Clock

import settings


try:
    switch = sys.argv[1]
except IndexError:
    switch = 'help'

options = []
for arg in sys.argv:
    if arg.startswith('--'):
        options.append(arg[2:])


def show_help():
    """Show help for CLI."""

    print("""Usage: python cannon.py command [options]

        Available commands:

        reload - Start listening on given port and save all coming requests
            to database. If there are already some requests recorded, you must
            use '--force' option.
        fire - Send all saved previously requests and send them to target
            address with proper arguments, headers and intervals.
        help - Show help.

    """)


def _checker(data):
    if data is None:
        return lambda i: False

    def inner(i):
        try:
            data.index(i)
            return True
        except ValueError:
            return False
    return inner


def load(opts=None):
    """Start recording http requests."""
    has_option = _checker(opts)

    if Bullet.count():
        if has_option('force'):
            Bullet.remove_all()
        else:
            print(
                "There are already records in database, use '--force' (Luke) "
                "to erase them, and start new recording.")
            exit(0)

    # Initialization of main clock.
    MainClock.initialize(Clock())

    app = tornado.web.Application([(r'/.*', RecordHandler)])
    app.listen(settings.config['port'])
    loop = tornado.ioloop.IOLoop.instance()
    loop.start()


if switch == 'reload':
    load(options)
elif switch == 'fire':
    pass
else:
    show_help()
