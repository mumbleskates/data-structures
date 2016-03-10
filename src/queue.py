# -*- coding: utf-8 -*-
from dll import Dll
from builtins import next, reversed


class Queue(object):
    def __init__(self, items=()):
        self._list = Dll(items)
        self._len = 0

    def __len__(self, other):
        return self._len

    def enqueue(self, item):
        self._len += 1
        self._list.append(item)

    def dequeue(self):
        self._len -= 1
        return self._list.pop()

    def peek(self):
        if not self._len:
            return None
        else:
            return next(reversed(self._list))

    size = __len__
