# coding=utf-8


class Graph(object):
    def __init__(self):
        self._dict = {}

    def nodes(self):
        """return a set of all nodes in the graph"""
        nodes_set = set()
        for key in self._dict:
            nodes_set.add(self._dict[key])
        return nodes_set

    def edges(self):
        """return a set of all edges in the graph"""
        edges_set = set()
        for key in self._dict:
            for value in self._dict[key]:
                edges_set.add((key, value))
        return edges_set

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
        return the set of all nodes connected to ‘n’ by edges, raises an error
        if n is not in g
        """
        # returns a copy so people can't mess with it
        return self._dict[n].copy()

    def adjacent(self, start, end):
        """
        return True if there is an edge connecting n1 and n2, False if not, raises an error
        if either of the supplied nodes are not in g
        """
        # check is end is in the Graph, returns KeyError
        self._dict[end]
        # check is end is in the node start set of the, returns KeyError
        return end in self._dict[start]
