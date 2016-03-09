# -*- coding: utf-8 -*-

import pytest

TEST_SET = [
    [],
    [1],
    [2, 3, 4],
]


@pytest.mark.parametrize("items", TEST_SET)
def test_append(items):
    from dll import Dll
    t_dll = Dll()
    for item in items:
        t_dll.append(item)
    assert list(t_dll) == list(items)


@pytest.mark.parametrize("items", TEST_SET)
def test_insert(items):
    from dll import Dll
    t_dll = Dll()
    for item in reversed(items):
        t_dll.append(item)
    assert list(t_dll) == list(items)


def test_remove():
    pass


def test_pop():
    pass


def test_shift():
    pass
