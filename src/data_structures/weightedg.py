# coding=utf-8
from heapq import heappush, heappop
from itertools import count

from data_structures.simpleg import Graph


class _GreatestValueCls(object):
    """
    The sole instance of this class always sorts before any other object, and is only equivalent to itself.
    """
    __slots__ = ()

    def __gt__(self, other):
        return True

    __ge__ = __gt__

    def __eq__(self, other):
        return other is _GreatestValue

    __le__ = __eq__

    def __lt__(self, other):
        return False

    def __str__(self):
        return "<Greatest value>"

    def __repr__(self):
        return "GreatestValue"

    __hash__ = object.__hash__

    def __add__(self, other):
        return self

    __radd__ = __add__

_GreatestValue = _GreatestValueCls()


class WeightedGraph(Graph):
    """Weighted graph data structure. Has nodes and edges between its nodes that have weights, typically the cost of
    traversing the edge. """

    def add_node(self, node):
        self._dict.setdefault(node, {})

    def del_node(self, n):
        """
        delete the node ‘n’ from the graph; raises a KeyError if no such node exists
        """
        # remove the node
        self._dict.pop(n)
        # remove any references to n
        for node in self._dict:
            self._dict[node].pop(n)

    def add_edge(self, start, end, weight=1):
        """
        add a new edge to the graph connecting ‘n1’ and ‘n2’. Weights must be summable and comparable, like numbers.

        If either n1 or n2 are not already present in the graph, they will be added.
        """
        try:
            0 < 0 + weight < 0 + weight + weight
        except TypeError:
            raise TypeError("Edge weights must be comparable and summable from zero!")

        self.add_node(start)
        self.add_node(end)
        self._dict[start][end] = weight

    def del_edge(self, start, end):
        del self._dict[start][end]

    def get_weight(self, start, end):
        """Returns a weight for a given edge defined by start and end. Raise a KeyError if the edge does not exist."""
        return self._dict[start][end]

    def edges_with_weights(self):
        """
        return a set of all edges in the graph with their weights as tuples in the format (from, to, weight)
        """
        return set(
            (node, neighbor, weight)
            for node in self._dict
            for neighbor, weight in self._dict[node].items()
        )

    def neighbors_with_weights(self, node):
        return self._dict[node].items()

    def dijkstra_traversal(self, start, end):
        """
        Returns a tuple of the total distance and the path taken to travel from the given start to end in the graph.

        The value returned is a 2-tuple of (cumulative distance, a list of nodes visited in order).

        If the given start does not exist in the graph, a KeyError is raised. If there is no path from start to end
        in the graph, the cumulative weight will be None and the path returned will be empty.
        """
        unique = count()
        visited = set()
        heap = [(0, None, start, ())]
        while heap:
            cumulative_weight, _, node, path = heappop(heap)
            if node not in visited:
                path = node, path
                if node == end:
                    return cumulative_weight, _convert_path(path)
                visited.add(node)
                for neighbor, edge_weight in self.neighbors_with_weights(node):
                    heappush(heap, (cumulative_weight + edge_weight, next(unique), neighbor, path))
        return None, []

    def bellman_ford(self, start):
        """
        Resolve all distances from the given start node to any other pathable node in the graph and return a tuple of
        2 dictionaries: a dictionary of all pathable nodes and the total distance of their shortest paths,
        and another that shows, for each node in these shortest paths, the previous step in
        """
        previous = {}
        distance = {node: _GreatestValue for node in self.nodes()}
        distance[start] = 0
        for _ in range(1, len(self._dict)):
            for node, neighbor, weight in self.edges_with_weights():
                if distance[neighbor] > (distance[node] + weight):
                    previous[neighbor] = node
                    distance[neighbor] = distance[node] + weight
        for node, neighbor, weight in self.edges_with_weights():
            if distance[node] + weight < distance[neighbor]:
                raise ValueError("Negative-weight cycle detected in graph")
        return distance, previous


def _convert_path(path):
    """Convert a reverse linked tuple path (3, (2, (1, ()))) to a forwards list [1, 2, 3]."""
    result = []
    while path:
        result.append(path[0])
        path = path[1]
    result.reverse()
    return result
