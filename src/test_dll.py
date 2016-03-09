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
        t_dll.insert(item)
    assert list(t_dll) == list(items)


TEST_SET_REMOVE = [
    ([1, 2, 3], 2, [1, 3]),
    ([1, 2, 3], 4, [1, 2, 3]),
    ([1, 2, 3, 2], 2, [1, 3, 2]),
]
@pytest.mark.parametrize("test_list, remove_me, result", TEST_SET_REMOVE)
def test_remove(test_list, remove_me, result):
    from dll import Dll
    t_dll = Dll(test_list)
    t_dll.remove(remove_me)
    assert list(t_dll) == result



def test_pop():
    pass


def test_shift():
    pass
