# coding=utf-8
from __future__ import unicode_literals, print_function
from builtins import range

import pytest

from data_structures.linked_list import LinkedList


CONSTRUCTOR_LISTS = [
    [],
    [1, 2, 3],
    [5],
    [3, 4, [3, 4, 5], 3, None],
    "asdf",
    [1, 1, 1, 1, 1],
]


@pytest.mark.parametrize('values', CONSTRUCTOR_LISTS)
def test_constructor(values):
    assert list(LinkedList(values)) == list(reversed(values))


def test_constructor_failure():
    # None is not iterable
    with pytest.raises(TypeError):
        LinkedList(None)


def test_empty_list():
    a_list = LinkedList()
    assert a_list.length == 0
    assert list(a_list) == []


def test_insert():
    a_list = LinkedList()
    a_list.insert(1)
    assert list(a_list) == [1]
    assert a_list.size() == 1


@pytest.mark.parametrize("items", CONSTRUCTOR_LISTS)
def test_pop(items):
    s = LinkedList(items)
    for item in reversed(items):
        assert s.pop() == item
    with pytest.raises(IndexError):
        s.pop()


def test_search():
    items = range(10)
    a_list = LinkedList(items)
    # searching for a non-contained item returns None
    assert a_list.search(object()) is None
    # prove those values are searchable
    for item in items:
        assert a_list.search(item).data == item


def test_remove():
    items = list(range(10))
    a_list = LinkedList(items)
    # removing a value that isn't in it should return false
    assert a_list.remove(object()) is False
    assert list(a_list) == list(reversed(items))
    # get 7 and remove it
    seven = a_list.search(7)
    assert a_list.remove(seven) is True
    assert list(a_list) == [9, 8, 6, 5, 4, 3, 2, 1, 0]
    # remove all the even-numbered values
    for node in a_list:
        if node & 1 == 0:
            assert a_list.remove(a_list.search(node)) is True
    assert list(a_list) == [9, 5, 3, 1]


@pytest.mark.parametrize("items", CONSTRUCTOR_LISTS)
def test_display(items, capfd):
    a_list = LinkedList(items)
    a_list.display()
    out, err = capfd.readouterr()
    assert out == str(tuple(reversed(items))) + '\n'
    assert not err
