# coding=utf-8

import pytest

def test_empty_list():
    from linked_list import LinkedList
    LinkedList()
    assert LinkedList().length == 0


def test_insert():
    from linked_list import LinkedList
    a_list = LinkedList()
    a_list.insert(1)
    assert list(a_list) == [1]
    a_list.insert(2)
    assert list(a_list) == [2, 1]


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
