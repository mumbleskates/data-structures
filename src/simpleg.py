# coding=utf-8


class Graph(object):
    def __init__(self):
        self._dict = {}

    def nodes(self):
        """return a list of all nodes in the graph"""
        nodes_list = []
        for key in self._dict:
            nodes_list.append(self._dict[key])
        return nodes_list

    def edges(self):
        """return a list of all edges in the graph"""
        edges_list = []
        for key in self._dict:
            for value in self._dict[key]:
                edges_list.append(key, value)
        return edges_list

    def add_edge(self, start, end):
        """
        adds a new edge to the graph connecting ‘n1’ and ‘n2’, if either n1 or n2 are not
        already present in the graph, they should be added.
        """
        existing_ends = self._dict[start]
        existing_ends.append(end)
        self._dict[start].update(existing_ends)

    def del_node(self, n):
        """deletes the node ‘n’ from the graph, raises an error if no such node exists"""
        pass

    def del_edge(self, start, end):
        """
        deletes the edge connecting ‘n1’ and ‘n2’ from the graph, raises an error if no
        such edge exists
        """
        existing_ends = self._dict[start]
        existing_ends.remove(end)
        self._dict[start].update(existing_ends)

    def has_node(self, n):
        """True if node ‘n’ is contained in the graph, False if not."""
        return bool(self._dict[n])

    def neighbors(self, n):
        """
        returns the list of all nodes connected to ‘n’ by edges, raises an error
        if n is not in g
        """
        return self._dict[n]

    def adjacent(self, start, end):
        """
        reurns True if there is an edge connecting n1 and n2, False if not, raises an error
        if either of the supplied nodes are not in g
        """
        if end in self._dict[start]:
            return True
        return False
