# coding=utf-8

from binheap import BinHeap
from itertools import count

# DONE: .insert(item): inserts an item into the queue.
# DONE: .pop(): removes the most important item from the queue.
# DONE: .peek(): returns the most important item without removing it from the queue.


class PriorityQ(object):
    def __init__(self):
        self._heap = BinHeap()
        self._unique = count()

    def insert(self, item, priority=1):
        self._heap.push((priority, next(self._unique), item))

    def pop(self):
        priority, _, item = self._heap.pop()
        return item

    def peek(self):
        priority, _, item = self._heap.peek()
        return item

