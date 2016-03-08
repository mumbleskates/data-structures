# coding=utf-8


class Node(object):
    def __init__(self, data=None, point=None):
        self.data = data
        self.point = point


class LinkedList(object):
        def __init__(self, items=()):
            self.head = Node()
            self.head.point = self.head
            self.length = 0
            for item in items:
                self.insert(item)

        def __iter__(self):
            n = self.head.point
            while n is not self.head:
                yield n.data
                n = n.point

        def insert(self, value):
            self.head.point = Node(value, self.head.point)
            self.length += 1

        def pop(self):
            first_node = self.head.point
            self.head.point = first_node.point
            self.length -= 1
            return first_node.data

        def size(self):
            return self.length

        def search(self, value):
            """
            Return the first node in the list with the data `value`,
            or None if not found
            """
            node = self.head.point
            while node is not self.head:
                if node.data == value:
                    return node
                node = node.point
            return None

        def remove(self, node):
            """
            Remove the given node from the list. Return True if it was removed,
            False if it was not found.
            """
            prev = self.head
            current = prev.point
            while current is not self.head:
                if current is node:
                    prev.point = current.point
                    self.length -= 1
                    return True
                # this isn't the node, advance
                prev, current = current, current.point
            return False

        def display(self):
            print("({})".format(
                ", ".join(map(repr, self))
            ))


# DONE: insert(val) will insert the value ‘val’ at the head of the list
# DONE: pop() will pop the first value off the head of the list and return it.
# DONE: size() will return the length of the list
# DONE: search(val) will return the node containing ‘val’ in the list, if present, else None
# DONE: remove(node) will remove the given node from the list, wherever it might be (node must be an item in the list)
# DONE: display() will print the list represented as a Python tuple literal: “(12, ‘sam’, 37, ‘tango’)”
