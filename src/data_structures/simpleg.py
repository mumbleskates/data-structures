# coding=utf-8
from collections import deque


class Graph(object):
    """Graph data structure. Has nodes and edges between its nodes."""

    def __init__(self):
        self._dict = {}

    def nodes(self):
        """return a set of all nodes in the graph"""
        return set(self._dict)

    def edges(self):
        """return a set of all edges in the graph"""
        return set((node, neighbor) for node in self._dict for neighbor in self._dict[node])

    def add_node(self, node):
        """add a new node to the graph"""
        self._dict.setdefault(node, set())

    def add_edge(self, start, end):
        """
        add a new edge to the graph connecting ‘n1’ and ‘n2’.

        If either n1 or n2 are not already present in the graph, they will be added.
        """
        self.add_node(start)
        self.add_node(end)
        self._dict[start].add(end)

    def del_node(self, n):
        """delete the node ‘n’ from the graph, or raise a KeyError if no such node exists"""
        # remove the node
        self._dict.pop(n)
        # remove any references to n
        for node in self._dict:
            self._dict[node].discard(n)

    def del_edge(self, start, end):
        """
        delete the edge connecting ‘n1’ and ‘n2’ from the graph, or raise a KeyError if no
        such edge exists
        """
        self._dict[start].remove(end)

    def has_node(self, n):
        """True if node ‘n’ is contained in the graph, False if not."""
        return n in self._dict

    def neighbors(self, n):
        """return the set of all nodes connected to ‘n’ by edges, raises a KeyError if n is not in the graph"""
        # returns a copy so people can't mess with it
        return self._dict[n].copy()

    def adjacent(self, start, end):
        """
        return True if there is an edge connecting n1 and n2, False if not.

        Raise a KeyError if either of the supplied nodes are not in the graph.
        """
        # check is end is in the Graph, may raise KeyError
        _ = self._dict[end]
        # check is end is in the node start set of the, may raise KeyError
        return end in self._dict[start]

    def depth_first_traversal(self, start):
        """
        Returns a generator that performs a full depth-first traversal of the graph beginning at the given start node.
        """
        visited = set()
        stack = [start]
        # let's do this without call recursion
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                yield node
                for neighbor in self.neighbors(node):
                    stack.append(neighbor)

    def recursive_depth_first(self, start):
        """
        Like the other depth first traversal, but uses recursion. Maybe more readable, may crash your machine when
        stack depth is exceeded in larger graphs.
        """
        visited = set()
        results = []

        def traverse(node):
            visited.add(node)
            results.append(node)
            for neighbor in self.neighbors(node):
                if neighbor not in visited:
                    traverse(neighbor)

        traverse(start)
        return results

    def breadth_first_traversal(self, start):
        """
        Return a generator that performs a full breadth-first traversal of the graph, beginning at the given start
        node.
        """
        visited = set()
        q = deque((start,))
        while q:
            node = q.pop()
            if node not in visited:
                visited.add(node)
                yield(node)
                for neighbor in self.neighbors(node):
                    q.appendleft(neighbor)
