# coding=utf-8

import pytest

PROPER_PAREN_OPEN = [
    ("("),
    ("(()"),
    ("(((())"),
]


@pytest.mark.parametrize("arg", PROPER_PAREN_OPEN)
def test_proper_paren(arg):
    from paren import proper_paren
    assert proper_paren(arg) == 1


PROPER_PAREN_BALLANCED = [
    ("()"),
    ("(())"),
    ("()(())"),
    ("()()"),
]


@pytest.mark.parametrize("arg", PROPER_PAREN_BALLANCED)
def test_proper_paren(arg):
    from paren import proper_paren
    assert proper_paren(arg) == 0


PROPER_PAREN_CLOSED = [
    (")"),
    ("())"),
    ("()())"),
    ("(()))"),
]


@pytest.mark.parametrize("arg", PROPER_PAREN_CLOSED)
def test_proper_paren(arg):
    from paren import proper_paren
    assert proper_paren(arg) == -1
