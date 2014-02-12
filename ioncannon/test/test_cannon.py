"""Tests for main components."""

from .. import get_storage


def test_get_storage():
    first = get_storage()
    second = get_storage()

    assert first == second
    assert first['db'] is second['db']
    assert first['fs'] is second['fs']
