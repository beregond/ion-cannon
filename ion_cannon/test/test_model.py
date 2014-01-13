"""Test functions to record http requests."""

import pytest

from ..model import Bullet, Clock, MainClock
from ..error import NotFound, NoFile


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

    non_existing = identity[::2] + identity[1::2]
    assert non_existing != identity
    assert len(identity) > 1
    with pytest.raises(NotFound):
        Bullet.get_by_id(non_existing)


def test_get_by_id_with_uncorrect_id():
    _prepare()
    with pytest.raises(NotFound):
        Bullet.get_by_id('asdf')


def test_count_bullets():
    _prepare()

    x = Bullet()
    x.headers = 'test'
    x.uri = '/test'
    x.method = 'get'
    x.content = 'some content'
    x.time = 10
    x.save()

    assert Bullet.count() == 1

    x = Bullet()
    x.headers = 'headers'
    x.uri = '/other'
    x.method = 'post'
    x.content = 'other content'
    x.time = 100
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


def test_get_all_chronologically():
    _prepare()

    cursor = Bullet.get_all_chronologically()
    result = [x for x in cursor]
    assert len(result) == 0

    x = Bullet()
    x.headers = {"some_header": "some_value"}
    x.uri = '/test'
    x.method = 'get'
    x.content = 'some content'
    x.time = 1000
    x.save()

    x = Bullet()
    x.headers = {"some_header": "some_value"}
    x.uri = '/other'
    x.method = 'post'
    x.content = 'other content'
    x.time = 10
    x.save()

    x = Bullet()
    x.headers = {"some_header": "some_value2"}
    x.uri = '/other2'
    x.method = 'post'
    x.content = 'other content'
    x.time = 100
    x.save()

    assert Bullet.count() == 3

    cursor = Bullet.get_all_chronologically()

    y = next(cursor)
    assert y.time == 10
    assert y.headers == {"some_header": "some_value"}

    y = next(cursor)
    assert y.time == 100
    assert y.headers == {"some_header": "some_value2"}

    y = next(cursor)
    assert y.time == 1000
    assert y.headers == {"some_header": "some_value"}


def test_without_file():
    _prepare()

    x = Bullet()
    x.uri = '/test'
    x.method = 'get'
    x.time = 1000

    with pytest.raises(NoFile):
        x.get_file()

    x.save()

    y = Bullet.get_by_id(x.id)
    assert y.uri == x.uri
    assert y.file is None
    assert y.has_file() is False
    with pytest.raises(NoFile):
        y.get_file()


def test_remove_all():
    _prepare()

    x = Bullet()
    x.headers = {'key': 'value'}
    x.uri = '/test'
    x.method = 'get'
    x.content = 'some content'
    x.time = 10
    x.save()

    x = Bullet()
    x.headers = {'key': 'value'}
    x.uri = '/test'
    x.method = 'get'
    x.content = 'some content'
    x.time = 100
    x.save()

    assert Bullet.count() == 2
    Bullet.remove_all()
    assert Bullet.count() == 0
