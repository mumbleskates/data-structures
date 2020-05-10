# coding=utf-8
from __future__ import unicode_literals
from builtins import open, range, reversed

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
    [1, 0, 2],  # balanced
    [0, 1, 2],  # right right
    [2, 1, 0],  # left left
    [2, 0, 1],  # left right
    [0, 2, 1],  # right left
    BIGTREE_ITEMS,
]
TREE_INORDER = list(map(sorted, TREE_ITEMS))
TREE_REVERSEORDER = [list(reversed(x)) for x in TREE_INORDER]
TREE_PREORDER = [
    [],
    [1],
    [1, 2],
    [2, 1],
    [1, 0, 2],
    [1, 0, 2],
    [1, 0, 2],
    [1, 0, 2],
    [1, 0, 2],
    [12, 9, 5, 42, 13, 28, 137],
]
TREE_POSTORDER = [
    [],
    [1],
    [2, 1],
    [1, 2],
    [0, 2, 1],
    [0, 2, 1],
    [0, 2, 1],
    [0, 2, 1],
    [0, 2, 1],
    [5, 9, 28, 13, 137, 42, 12],
]
TREE_BREADTHFIRST = [
    [],
    [1],
    [1, 2],
    [2, 1],
    [1, 0, 2],
    [1, 0, 2],
    [1, 0, 2],
    [1, 0, 2],
    [1, 0, 2],
    [12, 9, 42, 5, 13, 137, 28],
]
TREE_EXPECTED_SIZE = [
    0,
    1,
    2,
    2,
    3,
    3,
    3,
    3,
    3,
    7,
]
TREE_EXPECTED_DEPTH = [
    0,
    1,
    2,
    2,
    2,
    2,
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
    0,
    0,
    0,
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


def check_invariants(bst):
    # generator that yields all nodes in a sub-tree
    def tree_nodes(n):
        if n is None:
            return
        yield n
        if n.left:
            for x in tree_nodes(n.left):
                yield x
        if n.right:
            for x in tree_nodes(n.right):
                yield x

    for node in tree_nodes(bst._head):
        # sorted invariant
        if node.left:
            assert node.left.val < node.val
        if node.right:
            assert node.right.val > node.val
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


@pytest.mark.parametrize('items, expected', zip(TREE_ITEMS, TREE_REVERSEORDER))
def test_reverseorder(items, expected):
    bst = BST(items)
    assert list(reversed(bst)) == expected


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


@pytest.mark.parametrize('items', TREE_ITEMS + [range(20)])
def test_deplete_from_head(items):
    """Deplete the tree by repeatedly removing the topmost value"""
    bst = BST(items)
    for expected_len in reversed(range(len(items))):
        head_val = bst._head.val
        bst.delete(head_val)
        assert head_val not in bst
        assert len(bst) == expected_len


def test_tree_balance():
    bst = BST(range(63))
    # items added in order should come out into a perfectly balanced tree
    assert bst.depth() == 6


def test_tree_indexing():
    bst = BST(range(100, 120))
    for i in range(20):
        assert bst[i] == i + 100


def test_tree_negative_indexing():
    bst = BST(range(100, 120))
    for i in range(1, 21):
        assert bst[-i] == 120 - i


@pytest.mark.parametrize('items', TREE_ITEMS + [range(20)])
def test_delete_index(items):
    for index in range(len(items)):
        bst = BST(items)
        to_remove = bst[index]
        del bst[index]
        assert len(bst) == len(items) - 1
        assert to_remove not in bst
        check_invariants(bst)


@pytest.mark.parametrize('items', TREE_ITEMS + [range(20)])
def test_delete_negative_index(items):
    length = len(items)
    for index in range(length):
        bst = BST(items)
        to_remove = bst[index - length]
        del bst[index - length]
        assert len(bst) == length - 1
        assert to_remove not in bst
        check_invariants(bst)


def test_tree_indexing_bad_index():
    bst = BST()
    with pytest.raises(IndexError):
        _ = bst[0]
    bst = BST(range(10))
    with pytest.raises(IndexError):
        _ = bst[-11]
    with pytest.raises(IndexError):
        _ = bst[10]
    with pytest.raises(TypeError):
        _ = bst[1.5]


def test_tree_delete_index_bad_index():
    bst = BST()
    with pytest.raises(IndexError):
        del bst[0]
    bst = BST(range(10))
    with pytest.raises(IndexError):
        del bst[-11]
    with pytest.raises(IndexError):
        del bst[10]
    with pytest.raises(TypeError):
        del bst[1.5]


RANGE_BST = BST([1, 2, 3, 4, 0])
#       2
#     /  \
#    1    3
#   /      \
#  0        4
INCLUSIVES = [(True, True), (True, False), (False, True), (False, False)]


@pytest.mark.parametrize('inclusive', INCLUSIVES)
@pytest.mark.parametrize('i', range(5))
def test_irange_single_select(i, inclusive):
    assert list(RANGE_BST.irange(i, i, inclusive)) == ([i] if any(inclusive) else [])


@pytest.mark.parametrize('inclusive', INCLUSIVES)
@pytest.mark.parametrize('i', range(5))
def test_irange_single_select_surround(i, inclusive):
    assert list(RANGE_BST.irange(i - .5, i + .5, inclusive)) == [i]


@pytest.mark.parametrize('inclusive', INCLUSIVES)
@pytest.mark.parametrize('i', range(5 - 2))
def test_irange_several(i, inclusive):
    assert list(RANGE_BST.irange(i, i + 2, inclusive)) == (
        ([i] if inclusive[0] else []) +
        [i+1] +
        ([i+2] if inclusive[1] else [])
    )


@pytest.mark.parametrize('inclusive', INCLUSIVES)
@pytest.mark.parametrize('i', range(5))
def test_irange_open_start(i, inclusive):
    assert list(RANGE_BST.irange(None, i, inclusive)) == list(range(i + inclusive[1]))


@pytest.mark.parametrize('inclusive', INCLUSIVES)
@pytest.mark.parametrize('i', range(5))
def test_irange_open_stop(i, inclusive):
    assert list(RANGE_BST.irange(i, None, inclusive)) == list(range(i + (not inclusive[0]), 5))


@pytest.mark.parametrize('inclusive', INCLUSIVES)
def test_irange_open_both(inclusive):
    assert list(RANGE_BST.irange(None, None, inclusive)) == list(RANGE_BST)


@pytest.mark.parametrize('inclusive', INCLUSIVES)
def test_irange_outside_range_before(inclusive):
    assert list(RANGE_BST.irange(-2, -1, inclusive)) == []


@pytest.mark.parametrize('inclusive', INCLUSIVES)
def test_irange_outside_range_before_open(inclusive):
    assert list(RANGE_BST.irange(None, -1, inclusive)) == []


@pytest.mark.parametrize('inclusive', INCLUSIVES)
def test_irange_outside_range_after(inclusive):
    assert list(RANGE_BST.irange(10, 11, inclusive)) == []


@pytest.mark.parametrize('inclusive', INCLUSIVES)
def test_irange_outside_range_after_open(inclusive):
    assert list(RANGE_BST.irange(10, None, inclusive)) == []


@pytest.mark.parametrize('inclusive', INCLUSIVES)
@pytest.mark.parametrize('i', range(-1, 5))
def test_irange_between_values(i, inclusive):
    assert list(RANGE_BST.irange(i + .4, i + .6)) == []


@pytest.mark.parametrize('inclusive', INCLUSIVES)
@pytest.mark.parametrize('i', range(2, 5))
def test_irange_backwards_existing_values(i, inclusive):
    assert list(RANGE_BST.irange(i, i - 2, inclusive)) == []


@pytest.mark.parametrize('inclusive', INCLUSIVES)
@pytest.mark.parametrize('i', range(2, 5))
def test_irange_backwards_between_values(i, inclusive):
    assert list(RANGE_BST.irange(i + .5, i - 1.5, inclusive)) == []


def test_irange_empty_tree():
    assert list(BST().irange(1, 2)) == []


@pytest.mark.parametrize('items', TREE_ITEMS)
def test_clear(items):
    bst = BST(items)
    bst.clear()
    assert len(bst) == 0


@pytest.mark.parametrize('items', TREE_ITEMS)
def test_repr(items):
    bst = BST(items)
    if items:
        assert repr(bst) == str(bst) == "data_structures.bst.BST({0})".format(sorted(items))
    else:
        assert repr(bst) == str(bst) == "data_structures.bst.BST()"


def test_tree_invariants_fuzz():
    """Some (fuzz?) testing to ensure that nodes probably always hold the
    correct length of their sub-trees"""
    import random
    items = list(range(50))
    random.shuffle(items)
    bst = BST(items[:25])

    check_invariants(bst)

    for _ in range(200):
        bst.insert(random.randint(0, 49))
        check_invariants(bst)
        bst.delete(random.randint(0, 49))
        check_invariants(bst)
