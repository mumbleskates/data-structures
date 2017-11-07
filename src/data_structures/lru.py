# coding=utf-8


class _Node(object):
    __slots__ = ('key', 'val', 'cost', '_prev', '_next')

    def __init__(self, key, val, cost, prev, next_):
        self.key = key
        self.val = val
        self.cost = cost
        self._prev = prev
        self._next = next_

    def touch(self, sentinel):
        # remove self from DLL
        self._prev._next, self._next._prev = self._next, self._prev
        # insert self at the head
        self._prev, self._next = sentinel._prev, sentinel
        sentinel._prev._next, sentinel._prev = self, self

    def __repr__(self):  # pragma: no cover
        return "_Node({}, {}, {}, ..., ...)".format(self.key, self.val, self.cost)


# noinspection PyTypeChecker,PyUnresolvedReferences,PyDunderSlots,PyProtectedMember
class Lru(object):
    """
    A least-recently-used auto-evicting dict-like class.

    cost_func must be a function that accepts a key and a value and returns some metric of the item's storage cost.

    budget gets/sets the budget, which will be the limit for the sum of costs for all items in the Lru at any
    given time. current_cost gets the current total cost of the contained items.

    Accessing or setting an item updates its recency (but not checking if it's contained in the Lru).
    Items are always evicted least recent first, regardless of cost.
    Cost of an item is computed and stored when the value is set.
    """

    __slots__ = ('_dict', '_next', '_prev', '_budget', '_cost_func', '_current_cost')

    def __init__(self, items=(), budget=None, cost_func=lambda k, v: 1):
        """
        :param items: Optional iterable of key, value pairs to add in order. Defaults to empty.
        :param budget: Initial budget for contained items. Defaults to no limit.
        :param cost_func: Cost function for determining expense of a key/value pair. Defaults to always 1.
        """
        self._dict = {}
        self._next = self
        self._prev = self
        self._budget = budget if budget is not None else float('inf')
        if self.budget < 0:
            raise ValueError('budget must be non-negative')
        self._cost_func = cost_func
        self._current_cost = 0
        for k, v in items:
            self[k] = v

    def _remove_node(self, node):
        self._current_cost -= node.cost
        # delete node from DLL
        node._next._prev, node._prev._next = node._prev, node._next
        # delete node from dict
        del self._dict[node.key]

    def _evict(self):
        while self._current_cost > self._budget:
            self._remove_node(self._next)

    def __setitem__(self, key, value):
        cost = self._cost_func(key, value)
        if cost > self._budget:
            return  # instantly evict anything too costly to be stored
        self._current_cost += cost
        node = self._dict.get(key)
        if node:
            node.val = value
            self._current_cost -= node.cost
            node.cost = cost
            node.touch(self)
        else:
            prev = self._prev
            self._dict[key] = self._prev = prev._next = _Node(key, value, cost, prev, self)
        self._evict()

    def __getitem__(self, item):
        node = self._dict[item]
        node.touch(self)
        # unwrap the value
        return node.val

    def get(self, key, default=None):
        node = self._dict.get(key)
        if node is None:
            return default
        node.touch(self)
        return node.val

    def __delitem__(self, key):
        self._remove_node(self._dict[key])
        if not self._dict:
            # reset current cost to zero to avoid numeric instability
            self._current_cost = 0

    def __contains__(self, item):
        return item in self._dict

    def __len__(self):
        return len(self._dict)

    def __repr__(self):  # pragma: no cover
        return "Lru({})".format(list(self.items()) or "")

    @property
    def current_cost(self):
        """Current total cost of items held in the Lru."""
        return self._current_cost

    @property
    def budget(self):
        """Total budget that the Lru will evict down to when items are added."""
        return self._budget

    @budget.setter
    def budget(self, value):
        if value < 0:
            raise ValueError('budget must be non-negative')
        self._budget = value
        self._evict()

    def keys(self):
        return self._dict.keys()

    def __iter__(self):
        return iter(self._dict)

    def items(self):
        current = self._next
        while current is not self:
            yield current.key, current.val
            current = current._next
