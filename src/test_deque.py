# coding=utf-8
from __future__ import unicode_literals
from builtins import *

from itertools import count

import pytest


LISTS = [
    [],
    [1] * 10,
    [1, 2, 3] * 5,
    list(range(10)),
    list("asdfwablllllll"),
]


@pytest.mark.parametrize("items", LISTS)
def test_init(items):
    from deque import Deque
    d = Deque(items)
    assert list(d) == items
    assert list(reversed(d)) == list(reversed(items))


@pytest.mark.parametrize("items", LISTS)
def test_push_head(items):
    from deque import Deque
    d = Deque()
    for item in items:
        d.push_head(item)
    assert list(d) == list(reversed(items))
    assert list(reversed(d)) == items


@pytest.mark.parametrize("items", LISTS)
def test_pop_head(items):
    from deque import Deque
    d = Deque(items)
    for i, item in enumerate(items, 1):
        assert d.pop_head() == item
        assert len(d) == len(items) - i
    with pytest.raises(IndexError):
        d.pop_head()
    with pytest.raises(IndexError):
        d.pop_tail()


@pytest.mark.parametrize("items", LISTS)
def test_push_tail(items):
    from deque import Deque
    d = Deque()
    for item in items:
        d.push_tail(item)
    assert list(d) == items
    assert list(reversed(d)) == list(reversed(items))


@pytest.mark.parametrize("items", LISTS)
def test_pop_tail(items):
    from deque import Deque
    d = Deque(items)
    for i, item in enumerate(reversed(items), 1):
        assert d.pop_tail() == item
        assert len(d) == len(items) - i
    with pytest.raises(IndexError):
        d.pop_head()
    with pytest.raises(IndexError):
        d.pop_tail()


@pytest.mark.parametrize("items", LISTS)
def test_remove_first(items):
    from deque import Deque
    for val in set(items):
        d = Deque(items)
        assert d.remove_first(val)
        assert len(d) == len(items) - 1
        copy = list(items)
        copy.remove(val)
        assert list(d) == copy
        assert list(reversed(d)) == list(reversed(copy))
    d = Deque(items)
    assert not d.remove_first(object())
    assert len(d) == len(items)
    assert list(d) == items
    assert list(reversed(d)) == list(reversed(items))


@pytest.mark.parametrize("items", LISTS)
def test_remove_last(items):
    from deque import Deque
    for val in set(items):
        d = Deque(items)
        assert d.remove_last(val)
        assert len(d) == len(items) - 1
        copy = list(reversed(items))
        copy.remove(val)
        copy.reverse()
        assert list(d) == copy
        assert list(reversed(d)) == list(reversed(copy))
    d = Deque(items)
    assert not d.remove_first(object())
    assert len(d) == len(items)
    assert list(d) == items
    assert list(reversed(d)) == list(reversed(items))


@pytest.mark.parametrize("items", LISTS)
def test_remove_all(items):
    from deque import Deque
    for val in set(items):
        d = Deque(items)
        assert d.remove_all(val) == items.count(val)
        assert len(d) + items.count(val) == len(items)
        copy = [x for x in items if x != val]
        assert list(d) == copy
        assert list(reversed(d)) == list(reversed(copy))
    d = Deque(items)
    assert d.remove_all(object()) == 0
    assert len(d) == len(items)
    assert list(d) == items
    assert list(reversed(d)) == list(reversed(items))


@pytest.mark.parametrize("items", LISTS)
def test_clear(items):
    from deque import Deque
    d = Deque(items)
    assert d.clear() == len(items)
    assert len(d) == 0
    assert list(d) == list(reversed(d)) == []
