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


def test_push():
    pass


def test_pop():
    pass
