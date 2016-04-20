from data_structures.sort import insertion_sort
import pytest

UNSORTED_LISTS = [
    [5, 10, 3, 11, 12, 1, 7],
    [10, 100, 3, 12, 8, 19, 33],
    [],
    [3],
    [2, 3, 4]
]


SORTED_LISTS = list(map(sorted, UNSORTED_LISTS))


@pytest.mark.parametrize('items, expected', zip(UNSORTED_LISTS, SORTED_LISTS))
def test_insertion_sort(items, expected):
    items = list(items)
    insertion_sort(items)
    assert items == expected
