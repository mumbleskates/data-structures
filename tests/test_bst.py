# coding=utf-8
from __future__ import unicode_literals

import pytest

from data_structures.bst import BST


TREE_ITEMS = [
    [],
    [1],
    [1, 2],
    [2, 1],
    [12, 5, 9, 137, 42, 13, 28],
]

TREE_EXPECTED_SIZE = [
    0,
    1,
    2,
    2,
    7,
]

TREE_EXPECTED_DEPTH = [
    0,
    1,
    2,
    2,
    5,
]

TREE_EXPECTED_BALANCE = [
    0,
    0,
    -1,
    1,
    -2,
]


@pytest.mark.parametrize('items', TREE_ITEMS)
def test_init(items):
    BST(items)


@pytest.mark.parametrize('items', TREE_ITEMS)
def test_insert(items):
    bst = BST()
    for item in items:
        bst.insert(item)
    for item in items:
        assert item in bst


def test_insert_does_nothing():
    items = [12, 5, 9, 137, 42, 13, 28]
    bst = BST(items)
    assert len(bst) == 7
    for item in items:
        bst.insert(item)
    assert len(bst) == 7


def test_contains():
    items = [12, 5, 9, 137, 42, 13, 28]
    bst = BST(items)
    for item in items:
        assert item in bst
    assert not (1 in bst)


def test_contains_empty():
    bst = BST()
    assert not (1 in bst)


@pytest.mark.parametrize('items, expected', zip(TREE_ITEMS, TREE_EXPECTED_SIZE))
def test_size(items, expected):
    bst = BST(items)
    assert len(bst) == expected


@pytest.mark.parametrize('items, expected', zip(TREE_ITEMS, TREE_EXPECTED_DEPTH))
def test_depth(items, expected):
    bst = BST(items)
    assert bst.depth() == expected


@pytest.mark.parametrize('items, expected', zip(TREE_ITEMS, TREE_EXPECTED_BALANCE))
def test_balance(items, expected):
    bst = BST(items)
    assert bst.balance() == expected


@pytest.mark.parametrize('items', TREE_ITEMS)
def test_iterate(items):
    bst = BST(items)
    assert list(bst) == sorted(items)
