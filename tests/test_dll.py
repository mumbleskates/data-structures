# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from data_structures.dll import Dll


TEST_SET = [
    [],
    [1],
    [2, 3, 4],
]


@pytest.mark.parametrize("items", TEST_SET)
def test_append(items):
    t_dll = Dll()
    for item in items:
        t_dll.append(item)
    assert list(t_dll) == list(items)


@pytest.mark.parametrize("items", TEST_SET)
def test_insert(items):
    t_dll = Dll()
    for item in reversed(items):
        t_dll.insert(item)
    assert list(t_dll) == list(items)


TEST_SET_REMOVE = [
    ([1], 1, []),
    ([1, 2, 3], 2, [1, 3]),
    ([1, 2, 3, 2], 2, [1, 3, 2]),
]


@pytest.mark.parametrize("test_list, remove_me, result", TEST_SET_REMOVE)
def test_remove(test_list, remove_me, result):
    t_dll = Dll(test_list)
    t_dll.remove(remove_me)
    assert list(t_dll) == result


TEST_SET_REMOVE_ABSENT = [
    ([1, 2, 3], 4),
    ([], 4),
]


@pytest.mark.parametrize("items, remove_me", TEST_SET_REMOVE_ABSENT)
def test_remove_absent(items, remove_me):
    t_dll = Dll(items)
    with pytest.raises(ValueError):
        t_dll.remove(remove_me)
    assert list(t_dll) == items


POP_SHIFT_LISTS = [
    [1],
    [1, 2, 3, 4, 5],
]


@pytest.mark.parametrize("items", POP_SHIFT_LISTS)
def test_pop(items):
    t_dll = Dll(items)
    assert t_dll.pop() == items[0]
    assert list(t_dll) == items[1:]


def test_pop_empty():
    t_dll = Dll()
    with pytest.raises(IndexError):
        t_dll.pop()


@pytest.mark.parametrize("items", POP_SHIFT_LISTS)
def test_shift(items):
    t_dll = Dll(items)
    assert t_dll.shift() == items[-1]
    assert list(t_dll) == items[:-1]


def test_shift_empty():
    t_dll = Dll()
    with pytest.raises(IndexError):
        t_dll.shift()
