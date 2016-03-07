# coding=utf-8

class Node(object):
    def __init__(self, data=None, point=None):
        self.data = data
        self.point = point


class LinkedList(object):
        def __init__(self):
            self.head = Node()
            self.head.point = self.head
            self.length = 0

        def __iter__(self):
            n = self.head.point
            while n is not self.head:
                yield n.data
                n = n.point

        def insert(self, value):
            self.head.point = Node(value, self.head.point)
            self.length += 1

        def pop(self):
            firstNode = self.head.point
            self.head.point = firstNode.point
            self.length -= 1
            return firstNode.data

        def size(self):
            return self.length

        def search(self, value):
            pass

        def remove(self, node):
            pass

        def display(self):
            pass


# DONE: insert(val) will insert the value ‘val’ at the head of the list
# DONE: pop() will pop the first value off the head of the list and return it.
# DONE: size() will return the length of the list
# TODO: search(val) will return the node containing ‘val’ in the list, if present, else None
# TODO: remove(node) will remove the given node from the list, wherever it might be (node must be an item in the list)
# TODO: display() will print the list represented as a Python tuple literal: “(12, ‘sam’, 37, ‘tango’)”