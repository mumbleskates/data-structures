# coding=utf-8
from __future__ import unicode_literals, print_function
from builtins import map


class Node(object):
    def __init__(self, data=None, point=None):
        self.data = data
        self.point = point


class LinkedList(object):
    """
    A simple linked-list implementation
    """

    def __init__(self, items=()):
        """
        Create a new linked list.

        Optionally include an iterable of values to add to the list;
        after the list is built, the last item in the iterable will
        be at the front of the list.
        """
        self.head = Node()
        self.head.point = self.head
        self.length = 0
        for item in items:
            self.insert(item)

    def __iter__(self):
        """
        Iterate over the values of the elements in the list
        in pop-order (first to last)
        """
        n = self.head.point
        while n is not self.head:
            yield n.data
            n = n.point

    def insert(self, value):
        """Insert a new element at the front of the list with the given value"""
        self.head.point = Node(value, self.head.point)
        self.length += 1

    def pop(self):
        """Remove the first element in the list and return its value"""
        first_node = self.head.point
        if first_node is self.head:
            raise IndexError("Pop from no items")
        self.head.point = first_node.point
        self.length -= 1
        return first_node.data

    def size(self):
        """Return the number of elements in the list"""
        return self.length

    def search(self, value):
        """
        Return the first node in the list with the data `value`,
        or None if not found
        """
        node = self.head.point
        while node is not self.head:
            if node.data == value:
                return node
            node = node.point
        return None

    def remove(self, node):
        """
        Remove the given node from the list. Return True if it was removed,
        False if it was not found.
        """
        prev = self.head
        current = prev.point
        while current is not self.head:
            if current is node:
                prev.point = current.point
                self.length -= 1
                return True
            # this isn't the node, advance
            prev, current = current, current.point
        return False

    def display(self):
        """Print the contents of the list"""
        print("({})".format(
            ", ".join(map(repr, self)) +
            ("," if self.length == 1 else "")
        ))
