# -*- coding: utf-8 -*-
from .linked_list import LinkedList


class Stack(object):
    def __init__(self, items=()):
        self._list = LinkedList(items)

    # push() has the same functionality as insert()
    def push(self, item):
        self._list.insert(item)

    # pop() already has the desired functionality in LinkedList
    def pop(self):
        return self._list.pop()
