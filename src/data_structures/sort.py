# -*- coding: utf-8 -*-
from builtins import range


def insertion_sort(items):
    """Implementation of an in-place insertion sort algorithm."""
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


def merge_sort(items):
    """Return a generator that uses merge-sort to return the items of the list
    in sorted order."""
    def sub_sort(start, length):
        if length < 1:
            return
        if length == 1:
            yield items[start]
        else:
            left_length = length >> 1
            left = sub_sort(start, left_length)
            right = sub_sort(start + left_length, length - left_length)
            # fetch the first item from each side
            left_item = next(left)
            right_item = next(right)
            while True:
                if right_item < left_item:
                    yield right_item
                    # advance right side
                    try:
                        right_item = next(right)
                    except StopIteration:  # no more in right side
                        # read out all the items still in the left side
                        yield left_item
                        for remaining_item in left:
                            yield remaining_item
                        return
                else:
                    yield left_item
                    # advance left
                    try:
                        left_item = next(left)
                    except StopIteration:  # no more in left side
                        # read out all the items still in the right side
                        yield right_item
                        for remaining_item in right:
                            yield remaining_item
                        return

    return sub_sort(0, len(items))
