# coding=utf-8
from builtins import range

import pytest

from data_structures.binheap import BinHeap


TEST_ITEMS = [
    [],
    list(range(10)),
    list(reversed(range(10))),
    [1] * 5,
]


def assert_correct(heap, expected):
    # assert that the items come out as expected and in reverse sorted order
    expected = sorted(expected)
    while expected:
        assert heap.pop() == expected.pop()


@pytest.mark.parametrize("items", TEST_ITEMS)
def test_init(items):
    bh = BinHeap(items)
    assert_correct(bh, items)


@pytest.mark.parametrize("items", TEST_ITEMS)
def test_push(items):
    bh = BinHeap()
    parallel = []
    for item in items:
        bh.push(item)
        parallel.append(item)
    assert_correct(bh, parallel)
