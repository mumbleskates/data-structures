# coding=utf-8
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
