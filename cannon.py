"""Cannon to record and later send recorded http request to target url."""

import sys
import datetime
from functools import partial

import tornado.ioloop
import tornado.web
from logging.config import fileConfig

import settings
from ion_cannon.receive import RecordHandler, MonitorHandler
from ion_cannon.send import send
from ion_cannon.model import Bullet, Clock, MilisecondsClock
from ion_cannon.error import NotFound

fileConfig('logging.ini', disable_existing_loggers=False)

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
        monitor port - Monitor incoming requests at given port.
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
        elif has_option('continue'):
            # Proper initialization of main clock.
            try:
                latest = Bullet.get_latest()
                offset = latest.time + 100
            except NotFound:
                offset = 0

            clock = MilisecondsClock(offset=offset)
            Clock.initialize(clock)
        else:
            print(
                "There are already records in database, use '--force' (Luke) "
                "to erase them, and start new recording, or '--continue' "
                "to continue from 100 miliseconds after last recorded "
                "request.")
            exit(0)

    print('Started listening at port "{}"'.format(settings.config['port']))
    app = tornado.web.Application([(r'/.*', RecordHandler)])
    app.listen(settings.config['port'])
    loop = tornado.ioloop.IOLoop.instance()
    loop.start()


def fire():
    """Send recorded requests to target address."""
    loop = tornado.ioloop.IOLoop.instance()

    for item in Bullet.get_all_chronologically():
        func = partial(send, item.id)
        last_time = item.time
        loop.add_timeout(datetime.timedelta(0, 0, 0, item.time), func)

    def stop_loop():
        loop.stop()
    loop.add_timeout(datetime.timedelta(0, 0, 0, last_time + 100), stop_loop)
    loop.start()


def monitor(argv):
    """Monitor request on given address."""
    app = tornado.web.Application([(r'/.*', MonitorHandler)])
    app.listen(argv[2])
    loop = tornado.ioloop.IOLoop.instance()
    loop.start()


if switch == 'reload':
    load(options)
elif switch == 'fire':
    fire()
elif switch == 'monitor':
    monitor(sys.argv)
else:
    show_help()
