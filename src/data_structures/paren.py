# coding=utf-8
from __future__ import unicode_literals

# DONE: Return 1 if the string is “open” (there are open parens that are not closed)
# DONE: Return 0 if the string is “balanced” (there are an equal number of open and closed parentheses in the string)
# DONE: Return -1 if the string is “broken” (a closing parens has not been proceeded by one that opens)


def proper_paren(text):
    left_count = 0
    right_count = 0
    for char in text:
        if char == "(":
            left_count += 1
        if char == ")":
            right_count += 1
        if left_count < right_count:
            return -1
    if left_count > right_count:
        return 1
    else:
        return 0
