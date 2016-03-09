# coding=utf-8


class _Node(object):
    __slots__ = ('val', '_prv', '_nxt')

    def __init__(self, val, _prv, _nxt):
        self.val, self._prv, self._nxt = val, _prv, _nxt

    def remove(self):
        self._nxt._prv = self._prv
        self._prv._nxt = self._nxt


# noinspection PyProtectedMember
class Deque(object):
    def __init__(self, items=()):
        """
        Create a new Deque.

        An optional iterable of items will be added sequentially to
        the tail end of the deque.
        """
        self._prv = self._nxt = self
        self._len = 0
        for item in items:
            self.push_tail(item)

    def push_head(self, item):
        """Add an item to the head end of the deque"""
        head = self._nxt
        self._nxt = head._prv = _Node(item, self, head)
        self._len += 1

    def pop_head(self):
        """Remove and return the item at the head end of the deque"""
        if not self._len:
            raise IndexError("Pop from empty deque")
        new_head = self._nxt._nxt
        new_head._prv, self._nxt, result = self, new_head, self._nxt.val
        self._len -= 1
        return result

    def push_tail(self, item):
        """Add an item to the tail end of the deque"""
        tail = self._prv
        self._prv = tail._nxt = _Node(item, tail, self)
        self._len += 1

    def pop_tail(self):
        """Remove and return the item at the tail end of the deque"""
        if not self._len:
            raise IndexError("Pop from empty deque")
        new_tail = self._prv._prv
        new_tail._nxt, self._prv, result = self, new_tail, self._prv.val
        self._len -= 1
        return result

    def count(self, item):
        """Return the number of times an item exists in the deque"""
        return sum(1 for x in self if x == item)

    def remove_first(self, item):
        """
        Remove the first occurrence (from head) of an item from the deque.

        Returns True if an item was removed, False otherwise.
        """
        node = self._nxt
        while node is not self:
            if node.val == item:
                node.remove()
                self._len -= 1
                return True
            node = node._nxt
        else:
            return False

    def remove_last(self, item):
        """
        Remove the last occurrence (first from tail) of an item from the deque.

        Returns True if an item was removed, False otherwise.
        """
        node = self._prv
        while node is not self:
            if node.val == item:
                node.remove()
                self._len -= 1
                return True
            node = node._prv
        else:
            return False

    def remove_all(self, item):
        """
        Remove all occurrences of an item from the deque and return
        the number of items removed.
        """
        node = self._nxt
        original_len = self._len
        while node is not self:
            if node.val == item:
                node.remove()
                self._len -= 1
            node = node._nxt
        return original_len - self._len

    def clear(self):
        """
        Remove all items from the deque and return the number of items removed.
        """
        self._nxt = self._prv = self
        original_len = self._len
        self._len = 0
        return original_len

    def __len__(self):
        return self._len

    def __iter__(self):
        node = self._nxt
        while node is not self:
            yield node.val
            node = node._nxt

    def __reversed__(self):
        node = self._prv
        while node is not self:
            yield node.val
            node = node._prv

    def __repr__(self):
        if not self:
            return "Deque()"
        else:
            return "Deque([{}])".format(
                ", ".join(map(repr, self))
            )
