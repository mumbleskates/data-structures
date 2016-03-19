# coding=utf-8
from __future__ import unicode_literals

import pytest

from data_structures.paren import proper_paren


PROPER_PAREN_OPEN = [
    "(",
    "(()",
    "(((())",
]


@pytest.mark.parametrize("arg", PROPER_PAREN_OPEN)
def test_proper_paren(arg):
    assert proper_paren(arg) == 1


PROPER_PAREN_BALLANCED = [
    "()",
    "(())",
    "()(())",
    "()()",
]


@pytest.mark.parametrize("arg", PROPER_PAREN_BALLANCED)
def test_proper_paren(arg):
    assert proper_paren(arg) == 0


PROPER_PAREN_CLOSED = [
    ")",
    "())",
    "()())",
    "(()))",
]


@pytest.mark.parametrize("arg", PROPER_PAREN_CLOSED)
def test_proper_paren(arg):
    assert proper_paren(arg) == -1
