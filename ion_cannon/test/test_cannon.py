"""Tests for main components."""

from .. import get_storage

import settings


def test_get_storage():
    first = get_storage()
    second = get_storage()

    assert first == second
    assert first['db'] is second['db']
    assert first['fs'] is second['fs']


def test_get_storage_for_test():
    first = get_storage()

    old_value = settings.TEST
    settings.TEST = not old_value

    second = get_storage()

    assert first != second
    assert first['db'] is not second['db']
    assert first['fs'] is not second['fs']

    # Cleanup.
    settings.TEST = old_value
