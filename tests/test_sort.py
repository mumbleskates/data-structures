# coding=utf-8
import pytest
from data_structures.sort import insertion_sort, merge_sort


UNSORTED_LISTS = [
    [],
    [1],
    [1, 1],
    [1, 2],
    [2, 1],
    [2, 3, 4],
    [3, 2, 1],
    [5, 10, 3, 11, 12, 1, 7],
    [10, 100, 3, 12, 8, 19, 33],
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
