# coding=utf-8
from __future__ import unicode_literals
from builtins import open

from itertools import count
import pytest

from data_structures.bst import BST

# Our big-ish tree, constructed naiively, is shaped like so if populated naiively:
#            12
#          /    \
#        5       137
#         \      /
#          9   42
#             /
#            13
#             \
#              28
#
#
# If populated while balancing, it looks like so:
#      12
#
#      12
#     /
#    5
#
#      9
#     / \
#    5   12
#
#      9
#     / \
#    5   12
#          \
#          137
#
#      9
#     / \
#    5   42
#       /  \
#      12  137
#
#      9
#     / \
#    5   42
#       /  \
#      12  137
#       \
#        13...
#
# (Here a double rotation is performed)
#
#      12
#     /  \
#    9   42
#   /   /  \
#  5   13  137
#
#      12
#     /  \
#    9   42
#   /   /  \
#  5   13  137
#       \
#        28
#
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
    [12, 9, 5, 42, 13, 28, 137],
]
TREE_POSTORDER = [
    [],
    [1],
    [2, 1],
    [1, 2],
    [0, 2, 1],
    [5, 9, 28, 13, 137, 42, 12],
]
TREE_BREADTHFIRST = [
    [],
    [1],
    [1, 2],
    [2, 1],
    [1, 0, 2],
    [12, 9, 42, 5, 13, 137, 28],
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
    4,
]
TREE_EXPECTED_BALANCE = [
    0,
    0,
    -1,
    1,
    0,
    -1,
]


def get_full_dot(node):
    """return the tree with root 'self' as a dot graph for visualization"""
    return "digraph G{{\n{0}}}".format("" if node.val is None else (
        "\t{0};\n{1}\n".format(
            node.val,
            "\n".join(get_dot(node, count()))
        )
    ))


def get_dot(node, unique):
    """recursively prepare a dot graph entry for this node."""
    if node.left is not None:
        yield "\t{0} -> {1};".format(node.val, node.left.val)
        for i in get_dot(node.left, unique):
            yield i
    elif node.right is not None:
        r = next(unique)
        yield "\tnull{0} [shape=point];".format(r)
        yield "\t{0} -> null{1};".format(node.val, r)
    if node.right is not None:
        yield "\t{0} -> {1};".format(node.val, node.right.val)
        for i in get_dot(node.right, unique):
            yield i
    elif node.left is not None:
        r = next(unique)
        yield "\tnull{0} [shape=point];".format(r)
        yield "\t{0} -> null{1};".format(node.val, r)


def output_tree_dot(tree, filename="tree.dot"):
    """Output the DOT code for a BST tree to a file"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(get_full_dot(tree._head))


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


def test_insert_mutable():
    bst = BST()
    with pytest.raises(TypeError):
        bst.insert([])


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


def test_tree_balance():
    bst = BST(range(63))
    # items added in order should come out into a perfectly balanced tree
    assert bst.depth() == 6


def test_tree_invariants():
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
            # lengths should be always correct
            assert len(node) == sum((
                1,
                len(node.left) if node.left else 0,
                len(node.right) if node.right else 0
            ))
            # tree should always be balanced
            assert -1 <= node.balance <= 1
            # depths should always be correct
            assert node.depth == 1 + max(
                node.left.depth if node.left else 0,
                node.right.depth if node.right else 0
            )

    check_correct_lengths()

    for _ in range(200):
        bst.insert(random.randint(0, 49))
        check_correct_lengths()
        bst.delete(random.randint(0, 49))
        check_correct_lengths()
