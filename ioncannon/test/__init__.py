"""Tests."""

from ioncannon import set_storage


def switch_to_test_db():
    """Switch default storage to test storage."""
    set_storage('test_mongo')
