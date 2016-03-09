# -*- coding: utf-8 -*-

#DONE: insert(val) will insert the value ‘val’ at the head of the list
#DONE: append(val) will append the value ‘val’ at the tail of the list
#TODO: pop() will pop the first value off the head of the list and return it.
#TODO: shift() will remove the last value from the tail of the list and return it.
#DONE: remove(val) will remove the first instance of ‘val’ found in the list, starting from the head. If ‘val’ is
# not present, it will raise an appropriate Python exception.


class Node(object):
    def __init__(self, data=None, _prev=None, _next=None,):
        self.data = data
        self._prev = _prev
        self._next = _next

    def remove(self):
        self._next._prev = self._prev
        self._prev._next = self._next

# We're only accessing _next and _prev in the Node class
# noinspection PyProtectedMember
class Dll(object):
    """
    A simple double-ly linked-list implementation
    """

    def __init__(self, items=()):
        """
        Create a new double-ly linked list.

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

    def append(self, value):
        """Append a new element at the back of the list with the given value"""
        current_tail = self._prev
        new_node = Node(value, current_tail, self)
        current_tail._next = new_node
        self._prev = new_node

    def insert(self, value):
        """Insert a new element at the front of the list with the given value"""
        current_head = self._next
        new_node = Node(value, self, current_head)
        current_head._prev = new_node
        self._next = new_node

    def remove(self, value):
        n = self._next
        while n is not self:
            if value == n.data:
                n.remove()
                return
            n = n._next

    def pop(self):
        pass

    def shift(self):
        pass