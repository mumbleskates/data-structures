# coding=utf-8

class Grapgh(object):
    def __init__(self):
        pass

    def nodes(self):
        """return a list of all nodes in the graph"""
        pass

    def edges(self):
        """return a list of all edges in the graph"""
        pass

    def add_edge(self, _start, _end):
        """
        adds a new edge to the graph connecting ‘n1’ and ‘n2’, if either n1 or n2 are not
        already present in the graph, they should be added.
        """
        pass

    def del_node(self, n):
        """deletes the node ‘n’ from the graph, raises an error if no such node exists"""
        pass

    def del_edge(self, _start, _end):
        """
        deletes the edge connecting ‘n1’ and ‘n2’ from the graph, raises an error if no
        such edge exists
        """
        pass

    def has_node(self, n):
        """True if node ‘n’ is contained in the graph, False if not."""
        pass

    def neighbors(self, n):
        """
        returns the list of all nodes connected to ‘n’ by edges, raises an error
        if n is not in g
        """
        pass

    def adjacent(self, _start, _end):
        """
        reurns True if there is an edge connecting n1 and n2, False if not, raises an error
        if either of the supplied nodes are not in g
        """
        pass
