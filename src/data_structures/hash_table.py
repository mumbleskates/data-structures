# -*- coding: utf-8 -*-

try:
    # expected NameError
    # noinspection PyUnresolvedReferences
    STR_TYPES = (str, unicode)
except NameError:  # pragma: no cover
    STR_TYPES = (bytes, str)


class HashTable(object):
    """A variation of the Bernstein hash table algorithm."""

    def __init__(self):
        """Create a hash table with fized size of 1024."""
        self._table = [None] * 1024

    def get(self, key):
        """Return the value stored with the given key."""
        if not isinstance(key, STR_TYPES):
            raise TypeError(key, type(key), "Keys must be strings")
        i = self._hash(key)
        if self._table[i]:
            # inspector thinks all _table items are None
            # noinspection PyTypeChecker
            for k, v in self._table[i]:
                if k == key:
                    return v
        raise KeyError(key)

    def set(self, key, val):
        """Store the given value using the given key."""
        if not isinstance(key, STR_TYPES):
            raise TypeError(key, type(key), "Keys must be strings")
        i = self._hash(key)
        if not self._table[i]:
            self._table[i] = [(key, val)]
        else:
            # inspector thinks all _table items are None
            # noinspection PyTypeChecker
            for bucket_index, (k, v) in enumerate(self._table[i]):
                if k == key:
                    self._table[i][bucket_index] = (key, val)
                    break
            else:
                self._table[i].append((key, val))

    def _hash(self, key):
        """Hash the provided key."""
        mask = len(self._table) - 1
        h = 0
        for ch in key:
            h = (h * 33 + ord(ch)) & mask
        return h
