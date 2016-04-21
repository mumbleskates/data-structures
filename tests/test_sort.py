# coding=utf-8
import pytest
from data_structures.sort import insertion_sort, merge_sort, quicksort, merge_sort_2


UNSORTED_LISTS = [
    [],
    [1],
    [1, 1],
    [1, 2],
    [2, 1],
    [2, 3, 4],
    [3, 2, 1],
    [5, 10, 3, 11, 12, 1, 7],
    [10, 100, 12, 3, 8, 19, 33],
]
SORTED_LISTS = list(map(sorted, UNSORTED_LISTS))

STABILITY_KEY = str.lower
STABILITY_ITEMS = list('dBbaGDegEfAcFC')
STABILITY_SORTED = sorted(STABILITY_ITEMS, key=STABILITY_KEY)
assert STABILITY_SORTED != sorted(STABILITY_ITEMS)


@pytest.mark.parametrize('items, expected', zip(UNSORTED_LISTS, SORTED_LISTS))
def test_insertion_sort(items, expected):
    items = list(items)
    insertion_sort(items)
    assert items == expected


def test_insertion_sort_stability():
    items = list(STABILITY_ITEMS)
    insertion_sort(items, key=STABILITY_KEY)
    assert items == STABILITY_SORTED


@pytest.mark.parametrize('items, expected', zip(UNSORTED_LISTS, SORTED_LISTS))
def test_merge_sort(items, expected):
    assert list(merge_sort(items)) == expected


def test_merge_sort_stability():
    assert list(merge_sort(STABILITY_ITEMS, key=STABILITY_KEY)) == STABILITY_SORTED


@pytest.mark.parametrize('items, expected', zip(UNSORTED_LISTS, SORTED_LISTS))
def test_merge_sort_2(items, expected):
    items = list(items)
    merge_sort_2(items)
    assert items == expected


def test_merge_sort_2_stability():
    items = list(STABILITY_ITEMS)
    merge_sort_2(items, key=STABILITY_KEY)
    assert items == STABILITY_SORTED


@pytest.mark.parametrize('items, expected', zip(UNSORTED_LISTS, SORTED_LISTS))
def test_quicksort(items, expected):
    items = list(items)
    quicksort(items)
    assert items == expected


if __name__ == '__main__':
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
         "memory overall, but the space complexity is the same (O(n)).")
    ]:
        print()
        print(description)
        for trial in (small, medium, large):
            print("\t{0:.7f} seconds for {1} runs on a {2} item list".format(
                timeit(alg, number=RUN_COUNT),
                RUN_COUNT,
                len(trial)
            ))
