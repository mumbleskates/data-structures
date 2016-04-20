# -*- coding: utf-* -*-
from builtins import range


def insertion_sort(items):
    """Implementation of an inserstion sort algorithm."""
    for i, item in enumerate(items):
        for i in reversed(range(i)):
            compare_item = items[i]
            if item < compare_item:
                items[i + 1] = compare_item
            else:
                items[i + 1] = item
                break
                # we no longer need to move items
        else:
            items[0] = item
            # item was less than all the items before it
