# -*- coding: utf -8 -*-


class Trie(object):
    """Python implementation of trie data structure."""

    def __init__(self):
        """Create an empty trie."""
        self._edges = {}
        self._terminates = False

    def insert(self, token):
        """Insert token if not already in trie."""
        if not token:
            self._terminates = True
        else:
            child = self._edges.get(token[0])
            if child is None:
                child = self._edges[token[0]] = Trie()
            child.insert(token[1:])

    def contains(self, token):
        """Return true if token is in trie."""
        if not token:
            return self._terminates
        elif token[0] in self._edges:
            return self._edges[token[0]].contains(token[1:])
        else:
            return False
