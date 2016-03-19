# -*- coding: utf-8 -*-


class _Node(object):
    def __init__(self, data=None, _prev=None, _next=None,):
        self.data = data
        self._prev = _prev
        self._next = _next

    def remove_node(self):
        self._next._prev = self._prev
        self._prev._next = self._next


# We're only accessing _next and _prev in the Node class
# noinspection PyProtectedMember
class Dll(object):
    """
    A simple doubly linked-list implementation
    """

    def __init__(self, items=()):
        """
        Create a new doubly linked list.

        Optionally include an iterable of values to add to the list;
        after the list is built, the last item in the iterable will
        be at the front of the list.
        """
        self._prev = self
        self._next = self
        for item in items:
            self.append(item)

    def __iter__(self):
        """
        Iterate over the values of the elements in the list
        in pop-order (first to last)
        """
        n = self._next
        while n is not self:
            yield n.data
            n = n._next

    def __reversed__(self):
        """
        Iterate over the values of the elements in the list
        in shift-order (last to first)
        """
        n = self._prev
        while n is not self:
            yield n.data
            n = n._prev

    def append(self, value):
        """Append a new element at the back of the list with the given value"""
        current_tail = self._prev
        new_node = _Node(value, current_tail, self)
        current_tail._next = new_node
        self._prev = new_node

    def insert(self, value):
        """Insert a new element at the front of the list with the given value"""
        current_head = self._next
        new_node = _Node(value, self, current_head)
        current_head._prev = new_node
        self._next = new_node

    def remove(self, value):
        """Remove the first occurrence of value in the list"""
        n = self._next
        while n is not self:
            # noinspection PyArgumentList
            if value == n.data:
                n.remove_node()
                return
            n = n._next
        else:
            raise ValueError("Dll.remove(x): x not in list")

    def pop(self):
        """Remove and return the first value in the list"""
        head = self._next
        if head == self:
            raise IndexError("Popped from an empty list")
        head.remove_node()
        return head.data

    def shift(self):
        """Remove and return the last value in the list"""
        tail = self._prev
        if tail is self:
            raise IndexError("Shifted from an empty list")
        tail.remove_node()
        return tail.data
