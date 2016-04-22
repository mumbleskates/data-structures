# -*- coding: utf-8 -*-
from builtins import range

from itertools import chain


try:
    # noinspection PyUnresolvedReferences
    _INT_TYPES = (int, long)
except NameError:  # pragma: no cover
    _INT_TYPES = (int,)


def insertion_sort(items, key=lambda x: x):
    """Implementation of an in-place insertion sort algorithm. Best case time complexity
    is O(1), averege and worst case are both O(n^2)."""
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
    in sorted order. Best case and worst case time complexity are both O(n log n).

    The algorithm is generally rather faster than quicksort, but requires more space."""
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
            left_key = key(left_item)
            right_item = next(right)
            right_key = key(right_item)
            while True:
                if right_key < left_key:
                    yield right_item
                    # advance right side
                    try:
                        right_item = next(right)
                        right_key = key(right_item)
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
                        left_key = key(left_item)
                    except StopIteration:  # no more in left side
                        # read out all the items still in the right side
                        yield right_item
                        for remaining_item in right:
                            yield remaining_item
                        return

    return sub_sort(0, len(items))


def merge_sort_2(items, key=lambda x: x):
    """Iterative implementation of merge sort with a scratch list. Mutates the given list to be sorted."""
    if len(items) < 2:
        return

    source = items
    scratch = [None] * len(items)

    # With mini-run widths that double every iteration:
    width = 1
    while width < len(items):
        for start in range(0, len(items), width * 2):
            # merge source[start:start+width] and source[start+width:start+width*2] into scratch
            mid = start + width
            if mid >= len(items):
                scratch[start:] = source[start:]
                continue
            left = start
            right = mid
            left_item = source[left]
            left_key = key(left_item)
            end = min(start + width + width, len(items))
            right_item = source[right]
            right_key = key(right_item)
            for merged in range(start, start + width * 2):
                if left_key <= right_key:
                    scratch[merged] = left_item
                    left += 1
                    if left == mid:  # copy remaining righthand items
                        scratch[right:end] = source[right:end]
                        break
                    left_item = source[left]
                    left_key = key(left_item)
                else:
                    scratch[merged] = right_item
                    right += 1
                    if right == end:  # copy remaining lefthand items
                        assert end - (merged + 1) == mid - left
                        scratch[merged + 1:end] = source[left:mid]
                        break
                    right_item = source[right]
                    right_key = key(right_item)
        # use the old source list as the new scratch
        source, scratch = scratch, source
        # double the width for the next iteration
        width <<= 1

    if items is not source:
        # copy our end results into the original list if we ended up with our results in the other
        items[:] = source


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
    """Sort the given list in-place with the quicksort algorithm. Best case time complexity
    is O(n log n), worst case (rare) is O(n^2)."""
    def sub_sort(start, end):
        # Start is the inclusive first index of the partition, and end
        # is the exclusive last index

        # choose the median of first, last, and middle to pivot
        # https://en.wikipedia.org/wiki/Quicksort#Choice_of_pivot
        if end - start < 2:  # do not sort 1 or less items
            return

        a, b, c = start, end - 1, (start + end) >> 1
        if items[a] <= items[b] <= items[c] or items[c] <= items[b] <= items[a]:
            pivot_index = b
        elif items[b] <= items[a] <= items[c] or items[c] <= items[a] <= items[b]:
            pivot_index = a
        else:
            pivot_index = c

        pivot_index = _partition(items, start, end, pivot_index)

        sub_sort(start, pivot_index)
        sub_sort(pivot_index + 1, end)

    sub_sort(0, len(items))


def _hex_length(positive_int):
    """Return the number of hexadecimal digits necessary to
    represent the given number."""
    return ((positive_int.bit_length() - 1) >> 2) + 1


def radix_sort(items, key=lambda x: x):
    """Sort the given list with the radix sort algorithm."""
    # something that keeps track of the length of the longest number
    # something that keepst track of which iteration we are doing
    digit_shift = 0
    longest_num = 0  # some value, largest's numbers number of digits
    # go over list once to determine the above
    have_longest_num = False
    while True:
        buckets = [[] for _ in range(16)]
        for item in items:
            item_key = key(item)
            # make sure key is a valid positive integer
            if not isinstance(item_key, _INT_TYPES) or item_key < 0:
                raise TypeError("Keys or items must be positive integers", item_key)
            digit = (item_key >> digit_shift * 4) & 15  # 0b1111, 0xf
            buckets[digit].append(item)
            if not have_longest_num:
                longest_num = max(longest_num, _hex_length(item_key))
                # longest number will eventually be the len of our longest num
        have_longest_num = True
        for i, item in enumerate(chain(*buckets)):
            items[i] = item
        digit_shift += 1
        if digit_shift >= longest_num:  # that was the last iteration
            break


if __name__ == '__main__':  # pragma: no cover
    import random
    from timeit import timeit

    RUN_COUNT = 100

    small = [random.randint(0, 1023) for _ in range(10)]
    medium = [random.randint(0, 1023) for _ in range(100)]
    large = [random.randint(0, 1023) for _ in range(1000)]

    print("-- Sorting algorithm module --")

    for alg, description in [
        (lambda: insertion_sort(list(trial)),
         "Insertion-sort is an in-place algorithm with O(n^2) average- & worst-case, O(n) best-case time complexity."),

        (lambda: list(merge_sort(trial)),
         "Merge-sort is a non in-place implementation of the algorithm with O(n log n) best- & worst-case time "
         "complexity."),

        (lambda: quicksort(list(trial)),
         "Quicksort is an in-place implementation of the algorithm with O(n log n) best- & average-case, "
         "O(n^2) worst-case time complexity."),

        (lambda: merge_sort_2(list(trial)),
         "Another mergesort implementation using iteration between two arrays instead of generators. Should use less "
         "memory overall, but the space complexity is the same (O(n))."),

        (lambda: radix_sort(list(trial)),
         "Radix sort is an efficient sorting algorithm that orders numbers by taking them apart digit by digit "
         "rather than comparing them directly. Time complexity is always a virtually constant O(n log k), where k is "
         "the length of the largest number (in this case, in hexadecimal).")
    ]:
        print()
        print(description)
        for trial in (small, medium, large):
            print("\t{0:.7f} seconds for {1} runs on a {2} item list".format(
                timeit(alg, number=RUN_COUNT),
                RUN_COUNT,
                len(trial)
            ))
