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
        self.update_depths()

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, node):
        self._right = node
        if node is not None:
            node.parent = self
        self.update_depths()

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

    @property
    def balance(self):
        left_depth = self.left.depth if self.left else 0
        right_depth = self.right.depth if self.right else 0
        return left_depth - right_depth

    def insert(self, item):
        """
        Ensure the item is in the tree below this node and return True if
        it was added, or False if it was already there
        """
        if item == self.val:
            return False
        elif item < self.val:
            if self.left:
                added = self.left.insert(item)
                self.len_ += added
                return added
            else:
                self.left = _BSTNode(item)
                self.len_ += 1
                return True
        else:
            if self.right:
                added = self.right.insert(item)
                self.len_ += added
                return added
            else:
                self.right = _BSTNode(item)
                self.len_ += 1
                return True

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
                next_node = self.right.min_node()
                # steal the value of the next node in order
                self.val = next_node.val
                # since we have stolen next_node's value and it can be quickly removed,
                # remove it from the tree by replacing it in its parent
                if next_node.parent.left is next_node:
                    next_node.parent.left = next_node.drop()
                else:
                    next_node.parent.right = next_node.drop()

                # this node is not being removed; exit before we update lengths again
                return self
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

        # if we reach here, know this node will be removed from the tree
        # and must propagate the reduced length upwards
        parent = self.parent
        while parent:
            parent.len_ -= 1
            parent = parent.parent

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
            return self
        else:
            if self.right:
                self.right = self.right.remove_val(val)
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
            self._head.insert(item)
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


