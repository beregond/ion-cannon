"""Test functions to record http requests."""

from ..model import Bullet


def test_count_bullets():
    Bullet.remove_all()
    assert Bullet.count() == 0

    x = Bullet()
    x.headers = 'test'
    x.address = '/test'
    x.method = 'get'
    x.content = 'some content'
    x.time = 10
    x.save()

    assert Bullet.count() == 1

    x = Bullet()
    x.headers = 'headers'
    x.address = '/other'
    x.method = 'post'
    x.content = 'other content'
    x.time = 100
    x.save()

    assert Bullet.count() == 2
