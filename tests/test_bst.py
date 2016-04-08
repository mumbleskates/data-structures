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
TREE_INORDER = list(map(sorted, TREE_ITEMS))
TREE_PREORDER = [
    [],
    [1],
    [1, 2],
    [2, 1],
    [12, 5, 9, 137, 42, 13, 28],
]
TREE_POSTORDER = [
    [],
    [1],
    [2, 1],
    [1, 2],
    [9, 5, 28, 13, 42, 137, 12],
]
TREE_BREADTHFIRST = [
    [],
    [1],
    [1, 2],
    [2, 1],
    [12, 5, 137, 9, 42, 13, 28],
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
BIGTREE_ITEMS = [12, 5, 9, 137, 42, 13, 28]


@pytest.fixture(scope='session')
def bigtree():
    return BST(BIGTREE_ITEMS)


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


@pytest.mark.parametrize('items, expected', zip(TREE_ITEMS, TREE_INORDER))
def test_inorder(items, expected):
    bst = BST(items)
    assert list(bst.in_order()) == expected


@pytest.mark.parametrize('items, expected', zip(TREE_ITEMS, TREE_PREORDER))
def test_preorder(items, expected):
    bst = BST(items)
    assert list(bst.pre_order()) == expected


@pytest.mark.parametrize('items, expected', zip(TREE_ITEMS, TREE_POSTORDER))
def test_postorder(items, expected):
    bst = BST(items)
    assert list(bst.post_order()) == expected


@pytest.mark.parametrize('items, expected', zip(TREE_ITEMS, TREE_BREADTHFIRST))
def test_breadthfirst(items, expected):
    bst = BST(items)
    assert list(bst.breadth_first()) == expected


@pytest.mark.parametrize('item', BIGTREE_ITEMS)
def test_delete_success(item, bigtree):
    assert item in bigtree
    bigtree.delete(item)
    assert item not in bigtree


@pytest.mark.parametrize('items', TREE_ITEMS)
def test_delete_noop(items):
    bst = BST(items)
    before_length = len(bst)
    bst.delete(-1)
    assert len(bst) == before_length
