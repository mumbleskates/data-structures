# coding=utf-8
from __future__ import unicode_literals

from collections import deque


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
        self.update_stats()

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, node):
        self._right = node
        if node is not None:
            node.parent = self
        self.update_stats()

    def update_stats(self):
        """Update the depth and size of this node's subtree."""
        self.depth = 1 + max(
            self.left.depth if self.left else 0,
            self.right.depth if self.right else 0
        )
        self.len_ = (
            1 +
            (self.left.len_ if self.left else 0) +
            (self.right.len_ if self.right else 0)
        )

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

    def pick_minimum(self):
        """
        Remove the node that contains the minimum value in this subtree.

        The returned value is a tuple of what this node should be replaced with
        and what the minimum value in the sub-tree was.
        """
        if self.left:
            self.left, value = self.left.pick_minimum()
            return self.rebalance(), value
        else:
            return self.right, self.val

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
                self.right, self.val = self.right.pick_minimum()
                return self.rebalance()
            else:
                # left child only
                return self.left
        else:
            # right child only or no children. If self.right is None, we want to return
            # None anyway.
            return self.right

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

    def get_index(self, index):
        if self.left:
            # inspector thinks self.left isn't sized
            # noinspection PyTypeChecker
            left_len = len(self.left)
            if index >= left_len:
                # skip over entire left tree
                index -= left_len
            else:
                return self.left.get_index(index)
        # we have skipped the left side
        if index == 0:
            return self.val
        else:
            index -= 1
        # we have skipped our own value as well now
        # it must be in the right side subtree
        return self.right.get_index(index)


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

    def __getitem__(self, index):
        """Get an item from the tree by index, in sorted order."""
        if not isinstance(index, int):
            raise TypeError("indices must be integers")
        if index < 0:
            # support negative indexing from the end
            index += len(self)
        if index < 0 or index >= len(self):
            raise IndexError
        return self._head.get_index(index)

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
