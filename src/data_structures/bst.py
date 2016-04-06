# coding=utf-8
from __future__ import unicode_literals


__doc__ = """\
Binary Search Tree module

Provides an implementation of a binary search tree. Runtime complexities
are as follows:

insert, contains: O(log(n)) generally, O(n) worst case
size: O(1)
depth, balance: O(n)"""


class _BSTNode(object):
    def __init__(self, value):
        self._left = None
        self._right = None
        self._val = value
        self._len = 1

    def insert(self, item):
        """
        Ensure the item is in the tree below this node and return True if
        it was added, or False if it was already there
        """
        if item == self._val:
            return False
        elif item < self._val:
            if self._left:
                added = self._left.insert(item)
                self._len += added
                return added
            else:
                self._left = _BSTNode(item)
                self._len += 1
                return True
        else:
            if self._right:
                added = self._right.insert(item)
                self._len += added
                return added
            else:
                self._right = _BSTNode(item)
                self._len += 1
                return True

    def __contains__(self, item):
        if item == self._val:
            return True
        elif item < self._val:
            return self._left and item in self._left
        else:
            return self._right and item in self._right

    def __len__(self):
        return self._len

    def in_order(self):
        """Traverse the subtree in-order."""
        if self._left:
            for item in self._left:
                yield item
        yield self._val
        if self._right:
            for item in self._right:
                yield item

    def pre_order(self):
        """Traverse the subtree pre-order."""
        yield self._val
        if self._left:
            for item in self._left:
                yield item
        if self._right:
            for item in self._right:
                yield item

    def post_order(self):
        """Traverse the subtree post-order."""
        if self._left:
            for item in self._left:
                yield item
        if self._right:
            for item in self._right:
                yield item
        yield self._val

    def depth(self):
        left_depth = self._left.depth() if self._left else 0
        right_depth = self._right.depth() if self._right else 0
        return 1 + max(left_depth, right_depth)

    def balance(self):
        left_depth = self._left.depth() if self._left else 0
        right_depth = self._right.depth() if self._right else 0
        return left_depth - right_depth


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
        """
        Insert an item into the BST. If it is already present, ignore.
        """
        if self._head:
            self._head.insert(item)
        else:
            self._head = _BSTNode(item)

    def contains(self, item):
        """
        Return True if the given item is in the tree.
        """
        return self._head and item in self._head

    __contains__ = contains

    def __iter__(self):
        if self._head:
            for item in self._head:
                yield item

    def size(self):
        """
        Return the number of items in the tree.
        """
        return len(self._head) if self._head else 0

    __len__ = size

    def depth(self):
        """
        Return the depth of the tree's lowest leaf node.
        """
        if self._head:
            return self._head.depth()
        else:
            return 0

    def balance(self):
        """
        Return the difference in depth of the left and right sides of the
        tree's head. 0 means balanced, positive means the left side is
        deeper, negative means the right side is deeper.
        """
        if self._head:
            return self._head.balance()
        else:
            return 0


if __name__ == '__main__':
    print(__doc__)
