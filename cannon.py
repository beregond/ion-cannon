"""Cannon to record and later send recorded http request to target url."""

import argparse
import datetime
from functools import partial

import tornado.ioloop
import tornado.web
from logging.config import fileConfig

import settings
from ioncannon.receive import RecordHandler, MonitorHandler
from ioncannon.send import send
from ioncannon.model import Bullet, Clock, MilisecondsClock
from ioncannon.error import NotFound

fileConfig('logging.ini', disable_existing_loggers=False)

HELP = """
    [reload|fire|tunnel|monitor]

    reload - Start listening on given port and save all coming requests
    to database. If there are already some requests recorded, you must
    use '--force' option.

    fire - Send all saved previously requests and send them to target
    address with proper arguments, headers and intervals.

    tunnel - simultaneusly load and fire request. In this mode application
    works like http proxy with recorder on one side.

    monitor - Monitor incoming requests at given port.
"""


def load(args, tunnel_=False):
    """Start recording http requests."""

    if Bullet.count():
        if args.force:
            Bullet.remove_all()
        elif args.append:
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
                "to erase them, and start new recording, or '--append' "
                "to continue from 100 miliseconds after last recorded "
                "request.")
            exit(0)

    print('Started listening at port "{}"'.format(settings.config['port']))

    app = tornado.web.Application(
        [(r'/.*', RecordHandler, {'tunnel': tunnel_})])
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


def monitor(args):
    """Monitor request on given address."""
    app = tornado.web.Application([(r'/.*', MonitorHandler)])
    app.listen(args.port)
    loop = tornado.ioloop.IOLoop.instance()
    loop.start()


def tunnel(args):
    """Tunnel requests and record them."""
    load(args, True)


parser = argparse.ArgumentParser()

parser.add_argument('action', help=HELP)
parser.add_argument('port', nargs='?', default=False)
parser.add_argument(
    '--force',
    action='store_const',
    const=True,
    default=False,
    help="for reload action, it erases previous records and starts again"
)
parser.add_argument(
    '--append',
    action='store_const',
    const=True,
    default=False,
    help="for reload action, it append new records after existing ones"
)

if __name__ == '__main__':
    arg = parser.parse_args()

    action = arg.action
    if action == 'reload':
        load(arg)
    elif action == 'fire':
        fire()
    elif action == 'monitor':
        monitor(arg)
    elif action == 'tunnel':
        tunnel(arg)
    else:
        print('Wrong action!')
