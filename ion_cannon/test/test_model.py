"""Test functions to record http requests."""

import pytest

from ..model import Bullet, Clock, MainClock


def _prepare():
    Bullet.remove_all()
    assert Bullet.count() == 0


def test_save_and_get_by_id():
    _prepare()

    x = Bullet()
    x.headers = {'key': 'value'}
    x.uri = '/test'
    x.method = 'get'
    x.content = 'some content'
    x.time = 10
    x.version = '1'
    assert x.id is None
    x.save()
    assert x.id is not None

    identity = x.id

    y = Bullet.get_by_id(identity)
    assert y is not None
    assert y.id == x.id
    assert y.headers is not None
    assert isinstance(y.headers, dict)
    assert y.uri is not None
    assert y.method is not None
    assert y.file is not None
    assert y.time is not None
    assert y.version is not None

    non_existing = identity[::2] + identity[1::2]
    assert non_existing != identity
    z = Bullet.get_by_id(non_existing)
    assert z is None


def test_get_by_id_with_uncorrect_id():
    _prepare()
    x = Bullet.get_by_id('asdf')
    assert x is None


def test_count_bullets():
    _prepare()

    x = Bullet()
    x.headers = 'test'
    x.uri = '/test'
    x.method = 'get'
    x.content = 'some content'
    x.time = 10
    x.version = '1'
    x.save()

    assert Bullet.count() == 1

    x = Bullet()
    x.headers = 'headers'
    x.uri = '/other'
    x.method = 'post'
    x.content = 'other content'
    x.time = 100
    x.version = '2'
    x.save()

    assert Bullet.count() == 2


def test_clock():
    x = Clock()
    t1 = x.check()
    t2 = x.check()
    t3 = x.check()

    assert t1 <= t2
    assert t2 <= t3


def test_main_clock():
    MainClock.cleanup()
    with pytest.raises(RuntimeError):
        MainClock.check()

    MainClock.initialize(Clock())
    x = MainClock.check()
    assert x is not None

    MainClock.initialize(Clock())
    x = MainClock.check()
    assert x is not None

    MainClock.cleanup()
    with pytest.raises(RuntimeError):
        MainClock.check()
