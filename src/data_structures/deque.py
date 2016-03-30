# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
from builtins import next

from .dll import Dll


class Deque(object):
    def __init__(self, items=()):
        """
        Create an empty Deque

        Or fill one with passed in items adding to the HEAD of the
        list. The last item will be the new HEAD.
        """
        self._list = Dll()
        self._len = 0
        for item in items:
            self.append(item)

    def __iter__(self):
        """
        Iterate over the values of the elements in the Dll
        in pop-order (first to last)
        """
        return iter(self._list)

    def __reversed__(self):
        """
        Iterate over the values of the elements in the Dll,
        last to first
        """
        return reversed(self._list)

    def __len__(self):
        return self._len

    def append(self, val):
        """
        adds a value to the front of the deque
        """
        self._list.append(val)
        self._len += 1

    def appendleft(self, val):
        """
        adds a value to the front of the deque
        """
        self._list.insert(val)
        self._len += 1

    def pop(self):
        """
        removes a value from the end of the deque and returns it (raises an exception if
        the deque is empty)
        """
        result = self._list.shift()
        self._len -= 1
        return result

    def popleft(self):
        result = self._list.pop()
        self._len -= 1
        return result

    def peek(self):
        """
        returns the next value that would be returned by pop but leaves the value in the
        deque (returns None if the deque is empty)
        """
        if not self._len:
            return None
        else:
            return next(reversed(self._list))

    def peekleft(self):
        """
        returns the next value that would be returned by popleft but leaves the value in
        the deque (returns None if the deque is empty)
        """
        if not self._len:
            return None
        else:
            return next(iter(self._list))

    def size(self):
        """
        returns the count of items in the queue (returns 0 if the queue is empty)
        """
        return self._len
