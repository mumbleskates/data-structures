# coding=utf-8

import pytest

# TODO: .insert(item): inserts an item into the queue.
# TODO: .pop(): removes the most important item from the queue.
# TODO: .peek(): returns the most important item without removing it from the queue.

TEST_ITEMS = [
    [],
    list(zip(range(10), range(10))),
    list(zip(reversed(range(10)), range(10))),
    [(1, i) for i in range(5)],

]


def assert_correct(priorityq, expected):
    # assert that the items come out as expected and in reverse sorted order
    expected = sorted(expected)
    while expected:
        assert priorityq.pop() == expected.pop()


@pytest.mark.parametrize("items", TEST_ITEMS)
def test_init(items):
    from priorityq import PriotityQ
    pq = PriotityQ(items)
    assert_correct(pq, items)

TEST_PRIORITY = [
    ((1,"first"), "first"),
    (((1, "first"), (2, "second"), (3, "third")), "third"),
]

@pytest.mark.parametrize("items, output", TEST_PRIORITY)
def test_insert(items, output):
    from priorityq import PriotityQ
    pq = PriotityQ(items)
    assert pq.pop() == output


def test_pop():
    pass


def test_peek():
    pass