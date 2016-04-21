# -*- coding: utf-8 -*-

try:
    # expected NameError
    # noinspection PyUnresolvedReferences
    STR_TYPES = (str, unicode)
except NameError:
    STR_TYPES = (bytes, str)


_INITIAL_SIZE = 8
_HASH_MASK = (1 << 64) - 1
_PERTURB_SHIFT = 5
_SPARSENESS = 0.75


class HashTable(object):
    """A variation of the Bernstein hash table algorithm."""

    def __init__(self):
        """Create an empty hash table."""
        self._table = [None] * _INITIAL_SIZE
        self._len = 0
        self._occupied = 0

    def _walk_slots(self, key):
        table_mask = len(self._table) - 1
        h = perturb = HashTable._hash(key)
        while True:
            h &= table_mask
            yield h
            h = h * 5 + 1 + perturb
            perturb >>= _PERTURB_SHIFT

    @staticmethod
    def _hash(key):
        """Hash the provided key."""
        h = 0
        for ch in key:
            h = (h * 33 + ord(ch)) & _HASH_MASK
        return h

    def get(self, key):
        """Return the value stored with the given key."""
        if not isinstance(key, STR_TYPES):
            raise TypeError(key, type(key), "Keys must be strings")
        for i in self._walk_slots(key):
            slot = self._table[i]
            if slot is None:
                raise KeyError(key)
            elif slot and slot[0] == key:
                return slot[1]  # return value

    def set(self, key, val):
        """Store the given value using the given key."""
        if not isinstance(key, STR_TYPES):
            raise TypeError(key, type(key), "Keys must be strings")
        for i in self._walk_slots(key):
            slot = self._table[i]
            if not slot:
                self._table[i] = key, val
                self._len += 1
                # check if we need to resize the table
                if slot is None:  # if it is () dummy we are not occupying more slots
                    self._occupied += 1
                    if self._occupied / len(self._table) > _SPARSENESS:
                        self._grow()
                return
            elif slot[0] == key:
                self._table[i] = key, val  # found a matching key entry, replace it
                return

    def delete(self, key):
        """Delete a key from the table or raise a KeyError."""
        if not isinstance(key, STR_TYPES):
            raise TypeError(key, type(key), "Keys must be strings")
        for i in self._walk_slots(key):
            slot = self._table[i]
            if slot is None:
                raise KeyError(key)
            elif slot and slot[0] == key:
                self._table[i] = ()  # replace with dummy
                self._len -= 1
                return

    def _grow(self):
        """Double the size of the hash table."""
        old_table = self._table
        self._table = [None] * (len(self._table) << 1)
        for slot in old_table:
            if slot:
                for i in self._walk_slots(slot[0]):
                    if self._table[i] is None:
                        self._table[i] = slot
                        break
        self._occupied = self._len
