"""Automated tasks."""

from __future__ import print_function

from invoke import task, run


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
