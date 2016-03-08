# -*- coding: utf-8 -*-
import pytest


# We are testing invalid arguments
# noinspection PyArgumentList
def test_init():
    from stack import Stack

    Stack()
    Stack([1])
    Stack([1, 2, 3, 4])
    Stack("abc")
    with pytest.raises(TypeError):
        Stack(1)
    with pytest.raises(TypeError):
        Stack(1, 2)
    with pytest.raises(TypeError):
        Stack([1, 2], 3, 4)


# We are testing invalid arguments
# noinspection PyArgumentList
def test_push():
    from stack import Stack

    s = Stack()

    s.push(1)
    assert s.pop() == 1

    with pytest.raises(TypeError):
        s.push(1, 2)

    s.push([1, 2])
    assert s.pop() == [1, 2]

    for i in range(100):
        s.push(i)
    assert s.pop() == 99


# We are testing invalid arguments
# noinspection PyArgumentList
def test_pop():
    from stack import Stack

    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

    s = Stack([1])
    with pytest.raises(TypeError):
        s.pop(1)
    assert s.pop() == 1
    with pytest.raises(IndexError):
        s.pop()

    s = Stack([1, 2])
    assert s.pop() == 2
    assert s.pop() == 1
    with pytest.raises(IndexError):
        s.pop()

    s = Stack("abc")
    assert s.pop() == 'c'
    assert s.pop() == 'b'
    assert s.pop() == 'a'
    with pytest.raises(IndexError):
        s.pop()
    with pytest.raises(IndexError):
        s.pop()
