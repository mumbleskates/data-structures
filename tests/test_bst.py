# coding=utf-8
from __future__ import unicode_literals

import pytest

from data_structures.bst import BST

# Our big-ish tree, constructed naiively, is shaped like so:
#            12
#          /    \
#        5       137
#         \      /
#          9   42
#             /
#            13
#             \
#              28

BIGTREE_ITEMS = [12, 5, 9, 137, 42, 13, 28]
TREE_ITEMS = [
    [],
    [1],
    [1, 2],
    [2, 1],
    [1, 0, 2],
    BIGTREE_ITEMS,
]
TREE_INORDER = list(map(sorted, TREE_ITEMS))
TREE_PREORDER = [
    [],
    [1],
    [1, 2],
    [2, 1],
    [1, 0, 2],
    [12, 5, 9, 137, 42, 13, 28],
]
TREE_POSTORDER = [
    [],
    [1],
    [2, 1],
    [1, 2],
    [0, 2, 1],
    [9, 5, 28, 13, 42, 137, 12],
]
TREE_BREADTHFIRST = [
    [],
    [1],
    [1, 2],
    [2, 1],
    [1, 0, 2],
    [12, 5, 137, 9, 42, 13, 28],
]
TREE_EXPECTED_SIZE = [
    0,
    1,
    2,
    2,
    3,
    7,
]
TREE_EXPECTED_DEPTH = [
    0,
    1,
    2,
    2,
    2,
    5,
]
TREE_EXPECTED_BALANCE = [
    0,
    0,
    -1,
    1,
    0,
    -2,
]


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


@pytest.mark.parametrize('items', TREE_ITEMS)
def test_delete_success(items):
    for item in items:
        bst = BST(items)
        before_length = len(bst)
        assert item in bst
        bst.delete(item)
        assert item not in bst
        assert len(bst) == before_length - 1


@pytest.mark.parametrize('items', TREE_ITEMS)
def test_delete_noop(items):
    bst = BST(items)
    before_length = len(bst)
    bst.delete(-1)
    assert len(bst) == before_length


def test_tree_lengths_rigorously():
    """Some (fuzz?) testing to ensure that nodes probably always hold the
    correct length of their sub-trees"""
    import random
    items = list(range(50))
    random.shuffle(items)
    bst = BST(items[:25])

    # generator that yields all nodes in a sub-tree
    def tree_nodes(node):
        yield node
        if node.left:
            assert node.left.parent is node
            for x in tree_nodes(node.left):
                yield x
        if node.right:
            assert node.right.parent is node
            for x in tree_nodes(node.right):
                yield x

    def check_correct_lengths():
        for node in tree_nodes(bst._head):
            assert len(node) == sum(1 for _ in tree_nodes(node))

    check_correct_lengths()

    for _ in range(50):
        bst.insert(random.randint(0, 49))
        check_correct_lengths()
        bst.delete(random.randint(0, 49))
        check_correct_lengths()
