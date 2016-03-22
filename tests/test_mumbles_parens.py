# coding=utf-8
from __future__ import unicode_literals

import pytest


STRINGS = [
    ("", False),
    ("()", False),
    ("()()()()", False),
    ("(())", False),
    ("(()", True),
    ("())", True),
    (")(", True),
]


@pytest.mark.parametrize(("val", "expected"), STRINGS)
def test_parens(val, expected):
    from data_structures.mumbles_parens import check_parens
    assert bool(check_parens(val)) == expected
