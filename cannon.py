"""Cannon to record and later send recorded http request to target url."""

import sys

import tornado.ioloop
import tornado.web


try:
    switch = sys.argv[1]
except IndexError:
    switch = 'help'


def show_help():
    """Show help for CLI."""

    print("""Usage: python cannon.py (reload|fire|help) [--force]

        reload - Start listening on given port and save all coming requests
            to database. If there are already some requests recorded, you must
            use '--force' option.
        fire - Send all saved previously requests and send them to target
            address with proper arguments, headers and intervals.
        help - Show help.

    """)


def load():
    pass


if switch == 'reload':
    load()
elif switch == 'fire':
    pass
else:
    show_help()
