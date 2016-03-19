# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from builtins import range

import pytest

from data_structures.stack import Stack


@pytest.mark.parametrize("params", [
    (),
    ([1],),
    ([1, 2, 3, 4],),
    ("abc",),
])
def test_init(params):
    Stack(*params)


@pytest.mark.parametrize("params", [
    (1,),
    (1, 2),
    ([1, 2], 3, 4),
])
def test_bad_init(params):
    with pytest.raises(TypeError):
        Stack(*params)


LISTS = [
    [],
    [1, 1, 1],
    list(range(10)),
    [[1, 2], [2, 3, 4]],
]


@pytest.mark.parametrize("items", LISTS)
def test_push(items):
    s = Stack()
    for item in items:
        s.push(item)
    for item in reversed(items):
        assert s.pop() == item


@pytest.mark.parametrize("items", LISTS)
def test_pop(items):
    s = Stack(items)
    for item in reversed(items):
        assert s.pop() == item
    with pytest.raises(IndexError):
        s.pop()
