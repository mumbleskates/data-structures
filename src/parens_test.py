# coding=utf-8
from __future__ import unicode_literals

import pytest


STRINGS = [
    ("", 0),
    ("()", 0),
    ("()()()()", 0),
    ("(())", 0),
    ("(()", 1),
    ("())", -1),
    (")(", -1),
]


@pytest.mark.parametrize(("val", "expected"), STRINGS)
def test_parens(val, expected):
    from parens import check_parens
    assert check_parens(val) == expected
