# coding=utf-8

from binheap import BinHeap
from itertools import count

# DONE: .insert(item): inserts an item into the queue.
# DONE: .pop(): removes the most important item from the queue.
# DONE: .peek(): returns the most important item without removing it from the queue.

class PriotityQ(object):
    def __init__(self, items=()):
        self._heap = BinHeap()
        self._unique = count()
        for item in items:
            self.insert(item)

    def insert(self, item, priority=1):
        self._heap.push((priority, next(self._unique), item))

    def pop(self):
        priority, item = self._heap.pop()
        return item

    def peek(self):
        priority, item = self._heap.peek()
        return item

