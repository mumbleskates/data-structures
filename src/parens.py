# coding=utf-8
from __future__ import unicode_literals


def check_parens(string):
    depth = 0
    for ch in string:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth < 0:
                return -1
    if depth > 0:
        return 1
    else:
        return 0
