# coding=utf-8
from __future__ import unicode_literals, print_function
from builtins import *

import pytest


CONSTRUCTOR_LISTS = [
    ([], []),
    ([1, 2, 3], [3, 2, 1]),
    ([5], [5]),
    ([3, 4, [3, 4, 5], 3, None], [None, 3, [3, 4, 5], 4, 3]),
    ("asdf", ['f', 'd', 's', 'a']),
    ([1, 1, 1, 1, 1], [1, 1, 1, 1, 1]),
]
@pytest.mark.parametrize('values, result', CONSTRUCTOR_LISTS)
def test_constructor(values, result):
    from linked_list import LinkedList
    assert list(LinkedList(values)) == result


def test_constructor_failure():
    from linked_list import LinkedList
    # None is not iterable
    with pytest.raises(TypeError):
        LinkedList(None)


def test_empty_list():
    from linked_list import LinkedList
    a_list = LinkedList()
    assert a_list.length == 0
    assert list(a_list) == []


def test_insert():
    from linked_list import LinkedList
    a_list = LinkedList()
    a_list.insert(1)
    assert list(a_list) == [1]
    assert a_list.size() == 1
    a_list.insert(2)
    assert list(a_list) == [2, 1]
    assert a_list.size() == 2


TEST_POP = {
    (1, 1),
    (55, 55),
    (123490872988582498572379827512423, 123490872988582498572379827512423)
}


@pytest.mark.parametrize("node_value, result", TEST_POP)
def test_pop(node_value, result):
    from linked_list import LinkedList
    a_list = LinkedList()
    a_list.insert(node_value)
    assert a_list.pop() == result


def test_search():
    from linked_list import LinkedList
    a_list = LinkedList()
    assert a_list.search(0) is None
    # insert some values
    for i in range(10):
        a_list.insert(i)
    # prove those values are searchable
    for i in range(10):
        assert a_list.search(i).data == i
    # prove the list is in the right order etc.
    assert list(a_list) == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    # prove that values that have not been added cause None to return
    assert a_list.search(100) is None


def test_remove():
    from linked_list import LinkedList
    a_list = LinkedList()
    assert a_list.remove(0) is False
    # insert some values
    for i in range(10):
        a_list.insert(i)
    assert list(a_list) == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    # get 7 and remove it
    seven = a_list.search(7)
    assert a_list.remove(seven) is True
    # 7 has already been removed so this should return False
    # because nothing happened
    assert a_list.remove(seven) is False
    assert list(a_list) == [9, 8, 6, 5, 4, 3, 2, 1, 0]
    # remove all the even-numbered values
    for node in a_list:
        if node & 1 == 0:
            assert a_list.remove(a_list.search(node)) is True
    assert list(a_list) == [9, 5, 3, 1]
    assert a_list.remove(100) is False
