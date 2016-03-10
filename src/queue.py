# -*- coding: utf-8 -*-
from dll import Dll
from builtins import next, reversed


class Queue(object):
    def __init__(self, items=()):
        self._list = Dll(items)
        self._len = 0

    def __len__(self):
        """
        return the size of the queue. Should return 0 if the queue is empty.
        """
        return self._len

    def enqueue(self, item):
        """
        adds value to the queue
        """
        self._len += 1
        self._list.append(item)

    def dequeue(self):
        """
        removes the correct item from the queue and returns its value (should raise an
        error if the queue is empty)
        """
        self._len -= 1
        return self._list.pop()

    def peek(self):
        """
        returns the next value in the queue without dequeueing it. If the queue is
        empty, returns None
        """
        if not self._len:
            return None
        else:
            return next(reversed(self._list))

    size = __len__
