# -*- coding: utf-8 -*-
from builtins import range


def insertion_sort(items, key=lambda x: x):
    """Implementation of an in-place insertion sort algorithm."""
    for i, item in enumerate(items):
        for i in reversed(range(i)):
            compare_item = items[i]
            if key(item) < key(compare_item):
                items[i + 1] = compare_item
            else:
                items[i + 1] = item
                break
                # we no longer need to move items
        else:
            items[0] = item
            # item was less than all the items before it


def merge_sort(items, key=lambda x: x):
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
                if key(right_item) < key(left_item):
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


def _median(a, b, c):
    """Choose the median sorted value of three values"""
    if a <= b <= c or c <= b <= a:
        return b
    elif b <= a <= c or c <= a <= b:
        return a
    else:
        return c


def quicksort(items):
    """Sort the given list in-place with the quicksort algorithm."""
    def sub_sort(start, end):
        # Start is the inclusive first index of the partition, and end
        # is the exclusive last index

        # choose the median of first, last, and middle to pivot
        # https://en.wikipedia.org/wiki/Quicksort#Choice_of_pivot
        if end - start < 2:  # do not sort 1 or less items
            return

        pivot = _median(
            items[start],  # first
            items[(start + end) >> 1],  # middle
            items[end - 1]  # last
        )

        # perform
        lo = start
        hi = end - 1
        while lo < hi:
            while items[lo] < pivot:
                lo += 1
            while pivot < items[hi]:
                hi -= 1
            # now, items[hi] <= pivot <= items[lo]
            # swap hi and lo
            items[lo], items[hi] = items[hi], items[lo]

        pivot_index = hi

        sub_sort(start, pivot_index)
        sub_sort(pivot_index + 1, end)

    sub_sort(0, len(items))
