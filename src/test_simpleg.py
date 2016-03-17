# coding=utf-8

import pytest


def test_nodes():
    """return a list of all nodes in the graph"""
    pass

def test_edges():
    """return a list of all edges in the graph"""
    pass

def test_add_edge(n1, n2):
    """
    adds a new edge to the graph connecting ‘n1’ and ‘n2’, if either n1 or n2 are not
    already present in the graph, they should be added.
    """
    pass

def test_del_node(n):
    """deletes the node ‘n’ from the graph, raises an error if no such node exists"""
    pass

def test_del_edge(n1, n2):
    """
    deletes the edge connecting ‘n1’ and ‘n2’ from the graph, raises an error if no
    such edge exists
    """
    pass

def test_has_node(n):
    """True if node ‘n’ is contained in the graph, False if not."""
    pass

def test_neighbors(n):
    """
    returns the list of all nodes connected to ‘n’ by edges, raises an error
    if n is not in g
    """
    pass

def test_adjacent(n1, n2):
    """
    reurns True if there is an edge connecting n1 and n2, False if not, raises an error
    if either of the supplied nodes are not in g
    """
    pass
