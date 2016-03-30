# coding=utf-8
from builtins import range

import pytest

from data_structures.priorityq import PriorityQ


TEST_ITEMS = [
    [],
    list(zip(range(10), range(10))),
    list(zip(reversed(range(10)), range(10))),
    [(1, i) for i in range(5)],
    [(1, object()) for _ in range(10)],  # unorderable items
]


def assert_correct(priorityq, expected):
    # assert that the items come out as expected and in reverse sorted order
    expected = sorted(expected)
    while expected:
        assert priorityq.pop() == expected.pop()


@pytest.mark.parametrize("items", TEST_ITEMS)
def test_init(items):
    pq = PriorityQ()
    for priority, item in items:
        pq.insert(item, priority)


TEST_PRIORITY = [
    ([(1, "first")], "first"),
    ([(1, "first"), (2, "second"), (3, "third")], "third"),
]


@pytest.mark.parametrize("items, output", TEST_PRIORITY)
def test_insert(items, output):
    pq = PriorityQ()
    for priority, item in items:
        pq.insert(item, priority)
    assert pq.pop() == output


PRIORITY_ORDERS = [
    list(range(10)),
    list(reversed(range(10))),
    [1] * 10,
]


@pytest.mark.parametrize("priorities", PRIORITY_ORDERS)
def test_pop(priorities):
    pq = PriorityQ()
    inserted = {}  # dictionary of item:priority
    for pri in priorities:
        item = object()
        inserted[item] = pri
        pq.insert(item, pri)

    # extract all the items in priority order (highest pri first)
    extracted = []
    try:
        while True:
            extracted.append(pq.pop())
    except IndexError:
        pass

    # we now have all the items in the pq popped into a list
    # the priorities they were inserted by should be in descending order:
    extracted_priorities = [inserted[x] for x in extracted]
    assert extracted_priorities == sorted(extracted_priorities, reverse=True)


@pytest.mark.parametrize("priorities", PRIORITY_ORDERS)
def test_peek(priorities):
    pq = PriorityQ()
    for pri in priorities:
        pq.insert(object(), pri)
    for _ in range(len(priorities)):
        assert pq.peek() == pq.pop()