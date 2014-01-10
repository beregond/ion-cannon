"""Automated tasks."""

from __future__ import print_function

import os
import sys
import re
import subprocess
from ConfigParser import ConfigParser
from functools import partial

from invoke import task, run

# For tests purpose.
MIN_COVERAGE = 90


def _collect_files():
    conf = ConfigParser()
    conf.read('setup.cfg')
    dirs = conf.get('pytest', 'norecursedirs')
    dirs = [d for d in dirs.split(' ') if len(d.strip()) > 0]
    excluded = '|'.join(dirs)
    excluded = excluded.replace('.', '\\.')
    excluded = excluded.replace('*', '.*')
    excluded = re.compile(excluded)

    matches = []
    directory = os.path.abspath(os.path.dirname(__file__))
    _collect_recursively(directory, matches, excluded)

    return matches


def _collect_recursively(directory, result, excluded):
    for name in os.listdir(directory):
        if not excluded.match(name):
            fullpath = os.path.join(directory, name)
            if re.search('\\.py$', name):
                result.append(fullpath)
            elif os.path.isdir(fullpath):
                _collect_recursively(fullpath, result, excluded)


def _run_for_each(command, args, stdout=None, print_args=False):
    result = []
    for arg in args:
        if print_args:
            print(arg)
        result.append(subprocess.call(command + [arg], stdout=stdout))
    return max(result)


@task()
def test():
    """Run test suite."""

    files = _collect_files()
    jobs = [
        partial(subprocess.call, ['py.test', '--cov', '.']),
        partial(_run_for_each, ['pep257'], files, stdout=subprocess.PIPE),
    ]

    result = []
    for job in jobs:
        result.append(job())

    # Special case for code coverage (to be able to print adequate info).
    status = subprocess.call(
        ['coverage', 'report', '--fail-under={0}'.format(MIN_COVERAGE)],
        stdout=subprocess.PIPE
    )
    result.append(status)

    if status:
        print("Code coverage is too low!")

    if any(result):
        print("Tests have failed!")
        sys.exit(1)


@task
def deploy():
    """Deploy app."""

    run('pip install -r requirements.txt')

    try:
        with open('settings.py', 'r'):
            print('Settings already exists, skipping...')
    except IOError:
        print('Creating settings file...')
        f1 = open('settings.py', 'w')
        f2 = open('settings_dist.py', 'r')
        f1.write(f2.read())
        f1.close()
        f2.close()
        print('Done.')
        print('Please fill in settings file.')

    try:
        with open('logging.ini', 'r'):
            print('Logging settings already exists, skipping...')
    except IOError:
        print('Creating logging settings file...')
        f1 = open('logging.ini', 'w')
        f2 = open('logging_dist.ini', 'r')
        f1.write(f2.read())
        f1.close()
        f2.close()
        print('Done.')


@task()
def htmlcov():
    """Generate test coverage html reports."""
    run('py.test --cov . --cov-report html')
