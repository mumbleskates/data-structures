# coding=utf-8
from __future__ import unicode_literals
from builtins import open

from collections import deque
from itertools import count


"""\
Binary Search Tree module

Provides an implementation of a binary search tree. Runtime complexities
are as follows:

insert, contains: O(log(n)) generally, O(n) worst case
size: O(1)
depth, balance: O(n)"""


class _BSTNode(object):
    def __init__(self, value):
        self.val = value
        self.parent = None
        self._left = None
        self._right = None
        self.len_ = 1
        self.depth = 1

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, node):
        self._left = node
        if node is not None:
            node.parent = self
        self.update_depths()
        self.update_sizes()

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, node):
        self._right = node
        if node is not None:
            node.parent = self
        self.update_depths()
        self.update_sizes()

    def update_depths(self):
        """Change the depth of this node to be at least a certain amount."""
        node = self
        while node:
            depth = 1 + max(
                node.left.depth if node.left else 0,
                node.right.depth if node.right else 0
            )
            if node.depth == depth:
                # everything is correct now
                return

            # depth is changing, continue updating upwards
            node.depth = depth
            node = node.parent

    def update_sizes(self):
        node = self
        while node:
            size = (
                1 +
                (node.left.len_ if node.left else 0) +
                (node.right.len_ if node.right else 0)
            )
            if node.len_ == size:
                return

            node.len_ = size
            node = node.parent

    @property
    def balance(self):
        left_depth = self.left.depth if self.left else 0
        right_depth = self.right.depth if self.right else 0
        return left_depth - right_depth

    def left_rotation(self):
        pivot = self.right
        self.right = pivot.left
        pivot.left = self
        return pivot

    def right_rotation(self):
        pivot = self.left
        self.left = pivot.right
        pivot.right = self
        return pivot

    def rebalance(self):
        """Check that this node is balanced and return what should go in its place"""
        balance = self.balance
        if balance < -1:  # https://goo.gl/q0VorO
            # right tree is deeper
            # perform left rotation
            if self.right.balance > 0:  # avoid right-left case
                self.right = self.right.right_rotation()
            return self.left_rotation()

        elif balance > 1:
            # left tree is deeper
            # perform right rotation
            if self.left.balance < 0:  # avoid left-right case
                self.left = self.left.left_rotation()
            return self.right_rotation()

        else:
            # tree is balanced
            return self

    def insert(self, item):
        """
        Ensure the item is in the tree below this node and return the node that should
        go in this node's place once the tree is balanced.
        """
        if item == self.val:
            return self
        elif item < self.val:
            if self.left:
                self.left = self.left.insert(item)
                return self.rebalance()
            else:
                self.left = _BSTNode(item)
                return self
        else:
            if self.right:
                self.right = self.right.insert(item)
                return self.rebalance()
            else:
                self.right = _BSTNode(item)
                return self

    def min_node(self):
        if self.left:
            return self.left.min_node()
        else:
            return self

    # We are only pulling node values from the right-hand tree on deletion,
    # so this code is unused

    #  def max_node(self):
    #     if self.right:
    #         return self.right.max_node()
    #     else:
    #         return self

    def drop(self):
        """
        Delete this node's value from the tree.

        Return the node that should go in this node's place, whether it is still
        this node or another that is being moved upwards.
        """
        if self.left:
            if self.right:
                # both children
                # steal the value of the next node in order
                next_node = self.right.min_node()
                self.val = next_node.val
                # since we have stolen next_node's value,
                # remove it from the tree
                self.right = self.right.remove_val(next_node.val)

                return self.rebalance()
            else:
                # left child only
                replace_with = self.left
        else:
            if self.right:
                # right child only
                replace_with = self.right
            else:
                # leaf node
                replace_with = None

        # finally, return the node that is going to go in this spot
        return replace_with

    def remove_val(self, val):
        """
        Remove the node containing the given value from the tree if it
        exists.

        Return the node that should go in this node's place, whether it is still
        this node or another that is being moved upwards.
        """
        # if this node holds the value, remove it
        if self.val == val:
            return self.drop()

        # otherwise recurse down to find the value
        elif val < self.val:
            if self.left:
                self.left = self.left.remove_val(val)
                return self.rebalance()
            else:
                return self
        else:
            if self.right:
                self.right = self.right.remove_val(val)
                return self.rebalance()
            else:
                return self

    def __contains__(self, item):
        if item == self.val:
            return True
        elif item < self.val:
            return self.left and item in self.left
        else:
            return self.right and item in self.right

    def __len__(self):
        return self.len_

    def in_order(self):
        """Traverse the subtree in-order."""
        if self.left:
            for item in self.left.in_order():
                yield item
        yield self.val
        if self.right:
            for item in self.right.in_order():
                yield item

    def pre_order(self):
        """Traverse the subtree pre-order."""
        yield self.val
        if self.left:
            for item in self.left.pre_order():
                yield item
        if self.right:
            for item in self.right.pre_order():
                yield item

    def post_order(self):
        """Traverse the subtree post-order."""
        if self.left:
            for item in self.left.post_order():
                yield item
        if self.right:
            for item in self.right.post_order():
                yield item
        yield self.val

    def get_dot(self):
        """return the tree with root 'self' as a dot graph for visualization"""
        return "digraph G{{\n{0}}}".format("" if self.val is None else (
            "\t{0};\n{1}\n".format(
                self.val,
                "\n".join(self._get_dot(count()))
            )
        ))

    def _get_dot(self, unique):
        """recursively prepare a dot graph entry for this node."""
        if self.left is not None:
            yield "\t{0} -> {1};".format(self.val, self.left.val)
            for i in self.left._get_dot(unique):
                yield i
        elif self.right is not None:
            r = next(unique)
            yield "\tnull{0} [shape=point];".format(r)
            yield "\t{0} -> null{1};".format(self.val, r)
        if self.right is not None:
            yield "\t{0} -> {1};".format(self.val, self.right.val)
            for i in self.right._get_dot(unique):
                yield i
        elif self.left is not None:
            r = next(unique)
            yield "\tnull{0} [shape=point];".format(r)
            yield "\t{0} -> null{1};".format(self.val, r)


class BST(object):
    """Binary Search Tree."""

    def __init__(self, items=()):
        """
        Create a new tree.
        If an iterable is passed, all of its items are added to the tree.
        """
        self._head = None
        for item in items:
            self.insert(item)

    def insert(self, item):
        """Insert an item into the BST. If it is already present, ignore."""
        hash(item)  # reject mutable items
        if self._head:
            self._head = self._head.insert(item)
        else:
            self._head = _BSTNode(item)

    def delete(self, item):
        """Delete an item from the BST if it exists."""
        if self._head:
            self._head = self._head.remove_val(item)

    def contains(self, item):
        """Return True if the given item is in the tree."""
        return self._head and item in self._head

    __contains__ = contains

    def in_order(self):
        """Traverse the tree in-order."""
        if self._head:
            for item in self._head.in_order():
                yield item

    __iter__ = in_order

    def pre_order(self):
        """Traverse the tree pre-order."""
        if self._head:
            for item in self._head.pre_order():
                yield item

    def post_order(self):
        """Traverse the tree post-order."""
        if self._head:
            for item in self._head.post_order():
                yield item

    def breadth_first(self):
        """Traverse the tree breadth-first."""
        if self._head:
            q = deque((self._head,))
            while q:
                node = q.pop()
                yield node.val
                if node.left:
                    q.appendleft(node.left)
                if node.right:
                    q.appendleft(node.right)

    def size(self):
        """Return the number of items in the tree."""
        # noinspection PyTypeChecker
        return len(self._head) if self._head else 0

    __len__ = size

    def depth(self):
        """Return the depth of the tree's lowest leaf node."""
        return self._head.depth if self._head else 0

    def balance(self):
        """
        Return the difference in depth of the left and right sides of the
        tree's head. 0 means balanced, positive means the left side is
        deeper, negative means the right side is deeper.
        """
        if self._head:
            return self._head.balance
        else:
            return 0

    def output(self, filename="tree.dot"):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self._head.get_dot())
