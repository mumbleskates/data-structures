# coding=utf-8
from __future__ import unicode_literals
from builtins import range

import pytest


def bidirectional_match(a, b):
    assert list(a) == list(b)
    assert list(reversed(a)) == list(reversed(b))


TEST_LISTS = [
    [],
    [1],
    [1] * 3,
    [1, 2, 3],
    [1, 2, 3] * 2,
    [1, 1, 1, 2],
]


@pytest.mark.parametrize("items", TEST_LISTS)
def test_init(items):
    from deque import Deque
    d = Deque(items)
    bidirectional_match(d, items)
    assert d.size() == len(items)


def test_append():
    from deque import Deque
    d = Deque()
    expected = []
    for item in range(5):
        d.append(item)
        expected.append(item)
        bidirectional_match(d, expected)


def test_appendleft():
    from deque import Deque
    d = Deque()
    expected = []
    for item in range(5):
        d.appendleft(item)
        expected.insert(item, 0)
        bidirectional_match(d, expected)


def test_pop():
    from deque import Deque
    d = Deque(range(5))
    expected = list(range(5))
    while expected:
        assert d.pop() == expected.pop()
        assert d.size() == len(expected)
        bidirectional_match(d, expected)
    with pytest.raises(IndexError):
        d.pop()
    assert d.size() == 0


def test_popleft():
    from deque import Deque
    d = Deque(range(5))
    expected = list(range(5))
    while expected:
        assert d.popleft() == expected.pop(0)
        assert d.size() == len(expected)
        bidirectional_match(d, expected)
    with pytest.raises(IndexError):
        d.popleft()
    assert d.size() == 0


def test_peek():
    from deque import Deque
    d = Deque(range(5))
    while d:
        peek = d.peek()
        assert d.pop() == peek
    assert d.peek() is None


def test_peekleft():
    from deque import Deque
    d = Deque(range(5))
    while d:
        peek = d.peekleft()
        assert d.popleft() == peek
    assert d.peekleft is None
