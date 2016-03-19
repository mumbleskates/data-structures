# coding=utf-8
from itertools import count

from .binheap import BinHeap


class PriorityQ(object):
    def __init__(self):
        self._heap = BinHeap()
        self._unique = count()

    def insert(self, item, priority=1):
        """insert(item): inserts an item into the queue."""
        self._heap.push((priority, next(self._unique), item))

    def pop(self):
        """pop(): removes the most important item from the queue."""
        priority, _, item = self._heap.pop()
        return item

    def peek(self):
        """peek(): returns the most important item without removing it from the queue."""
        priority, _, item = self._heap.peek()
        return item

