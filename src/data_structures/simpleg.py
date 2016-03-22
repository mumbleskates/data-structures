# coding=utf-8
from collections import deque


def once(x):
    yield x


class Graph(object):
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
        add a new edge to the graph connecting ‘n1’ and ‘n2’, if either n1 or n2 are not
        already present in the graph, they should be added.
        """
        self.add_node(start)
        self.add_node(end)
        self._dict[start].add(end)

    def del_node(self, n):
        """delete the node ‘n’ from the graph, raises an error if no such node exists"""
        # remove the node
        self._dict.pop(n)
        # remove any references to n
        for node in self._dict:
            self._dict[node].discard(n)

    def del_edge(self, start, end):
        """
        delete the edge connecting ‘n1’ and ‘n2’ from the graph, raises an error if no
        such edge exists
        """
        self._dict[start].remove(end)

    def has_node(self, n):
        """True if node ‘n’ is contained in the graph, False if not."""
        return n in self._dict

    def neighbors(self, n):
        """
        return the set of all nodes connected to ‘n’ by edges, raises an
        error if n is not in g
        """
        # returns a copy so people can't mess with it
        return self._dict[n].copy()

    def adjacent(self, start, end):
        """
        return True if there is an edge connecting n1 and n2, False if not, raises an error
        if either of the supplied nodes are not in g
        """
        # check is end is in the Graph, returns KeyError
        _ = self._dict[end]
        # check is end is in the node start set of the, returns KeyError
        return end in self._dict[start]

    def depth_first_traversal(self, start):
        """
        Perform a full depth-first traversal of the graph beginning at start.
        Return the full visited path when traversal is complete.
        """
        visited = set()
        stack = []
        current = once(start)
        # let's do this without call recursion
        while True:
            # get the next neighbor we haven't visited if there is one
            try:
                while True:
                    node = next(current)
                    if node not in visited:
                        break
            except StopIteration:
                # this stack frame is exhausted, move back up
                if stack:
                    current = stack.pop()
                else:  # we're completely finished
                    return
                continue

            # node is now a node we haven't visited yet
            visited.add(node)
            yield node
            stack.append(current)
            current = iter(self.neighbors(node))

    def recursive_depth_first(self, start):
        """
        Like the other depth first traversal, but uses recursion. Maybe more readable.
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
        Perform a full breadth-first traversal of the graph, beginning at start.
        Return the full visited path when traversal is complete.
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
