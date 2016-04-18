# -*- coding: utf-8 -*-

class HashTable(object):
    """A variation of the Bernstein hash table algorithm."""

    def __init__(self):
        """Create a hash table with fized size of 1024."""
        self._table = [None] * 1024

    def get(self, key):
        """Return the value stored with the given key."""
        if not isinstance(key, str):
            raise TypeError("Keys must be strings")
        i = self._hash(key)
        if self._table[i]:
            for k, v in self._table[i]:
                if k == key:
                    return v
        raise KeyError(key)

    def set(self, key, val):
        """Store the given value using the given key."""
        if not isinstance(key, str):
            raise TypeError("Keys must be strings")
        i = self._hash(key)
        if not self._table[i]:
            self._table[i] = [(key, val)]
        else:
            self._table[i].append((key, val))

    def _hash(self, key):
        """Hash the provided key."""
        mask = len(self._table) - 1
        h = 0
        for ch in key:
            h = (h * 33 + ord(ch)) & mask
        return h
