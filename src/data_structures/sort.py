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


def _partition(items, start, end, pivot_index):
    """Partition a range of a list across a pivot and return
    the new index of the pivot."""
    # move the pivot to the beginning of the range
    pivot = items[pivot_index]  # swap our pivot out to the first slot in the range
    items[start], items[pivot_index] = items[pivot_index], items[start]

    # perform partition over the pivot
    lo = start + 1  # start at the index after our pivot
    hi = end - 1  # start at the last index in the range
    while lo <= hi:
        while lo <= hi and pivot < items[hi]:  # find an item in the large side that doesn't belong
            hi -= 1
        while lo <= hi and items[lo] <= pivot:  # find an item on the small side that doesn't belong
            lo += 1
        if hi < lo:  # our ends have met, the partitioning is done
            break
        items[lo], items[hi] = items[hi], items[lo]  # swap ill fitting items to the correct sides
        lo += 1
        hi -= 1

    # move the pivot back to the center; the item at [hi] belongs in the low side at this point
    items[start], items[hi] = items[hi], items[start]
    return hi  # our pivot is now at [hi]


def quicksort(items):
    """Sort the given list in-place with the quicksort algorithm."""
    def sub_sort(start, end):
        # Start is the inclusive first index of the partition, and end
        # is the exclusive last index

        # choose the median of first, last, and middle to pivot
        # https://en.wikipedia.org/wiki/Quicksort#Choice_of_pivot
        if end - start < 2:  # do not sort 1 or less items
            return

        pivot_index = _partition(items, start, end, start)

        sub_sort(start, pivot_index)
        sub_sort(pivot_index + 1, end)

    sub_sort(0, len(items))
