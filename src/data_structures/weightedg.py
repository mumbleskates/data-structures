# coding=utf-8
from heapq import heappush, heappop
from itertools import count

from data_structures.simpleg import Graph


class WeightedGraph(Graph):
    def add_node(self, node):
        self._dict.setdefault(node, {})

    def del_node(self, n):
        """
        delete the node ‘n’ from the graph, raises an error if no such node
        exists
        """
        # remove the node
        self._dict.pop(n)
        # remove any references to n
        for node in self._dict:
            self._dict[node].pop(n)

    def add_edge(self, start, end, weight=1):
        """
        add a new edge to the graph connecting ‘n1’ and ‘n2’, if either n1
        or n2 are not already present in the graph, they should be added.
        """
        self.add_node(start)
        self.add_node(end)
        self._dict[start][end] = weight

    def del_edge(self, start, end):
        del self._dict[start][end]

    def get_weight(self, start, end):
        """
        Returns a weight for a given edge defined by start end
        """
        return self._dict[start][end]

    def edges_with_weights(self):
        """
        return a set of all edges in the graph with weights
        """
        return set(
            (node, neighbor, weight)
            for node in self._dict
            for neighbor, weight in self._dict[node].items()
        )

    def neighbors_with_weights(self, node):
        return self._dict[node].items()

    def dijkstra_traversal(self, start, end):
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


def _convert_path(path):
    """Convert a reverse linked tuple path (3, (2, (1, ()))) to a forwards list [1, 2, 3]."""
    result = []
    while path:
        result.append(path[0])
        path = path[1]
    result.reverse()
    return result
