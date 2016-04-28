# -*- coding: utf -8 -*-
from builtins import next, range, zip

from collections import deque


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
            child = self._edges.get(token[:1])
            if child is None:
                child = self._edges[token[:1]] = Trie()
            child.insert(token[1:])

    def contains(self, token):
        """Return true if token is in trie."""
        if not token:
            return self._terminates
        elif token[:1] in self._edges:
            return self._edges[token[:1]].contains(token[1:])
        else:
            return False

    __contains__ = contains

    # noinspection PyProtectedMember
    def __iter__(self):
        """Traversing the trie depth-first."""
        stack = (None, None, None, None)  # singly linked list stack of loop context vars
        node = self
        prefix = None
        edge_items = iter(node._edges.items())  # iterator over the edges
        while node is not None:
            try:
                edge, new_node = next(edge_items)
            except StopIteration:
                stack, node, prefix, edge_items = stack
            else:
                stack = (stack, node, prefix, edge_items)
                node = new_node
                prefix = edge if prefix is None else prefix + edge
                edge_items = iter(node._edges.items())
                if node._terminates:
                    yield prefix

    # noinspection PyProtectedMember
    def breadth_first(self, prefix=None):
        """Helper breadth first traversal function for auto complete."""
        q = deque()
        q.appendleft((self, prefix))
        while q:
            node, prefix = q.pop()
            if node._terminates:
                yield prefix
            for edge, child in node._edges.items():
                q.appendleft((child, edge if prefix is None else prefix + edge))

    def auto_complete(self, token, max_results=4):
        """Trie auto complete."""
        node = self
        prefix = token
        # traverse down until we have found the node that matches the given token
        while token:
            edge, token = token[:1], token[1:]
            if edge not in node._edges:
                return  # there are no entries with that prefix
            else:
                node = node._edges[edge]
        # iterate ovr the children breadth first from there
        # return default maximum of 4 tokens
        for item, _ in zip(node.breadth_first(prefix), range(max_results)):
            yield item


def _beginning_match(a, b):
    """Return the number of characters matching at the beginning of the two symbols"""
    matched = 0
    for ch_a, ch_b in zip(a, b):
        if ch_a != ch_b:
            break
        matched += 1
    return matched


class ShortTrie(object):
    """Python implementation of trie data structure that can have multiple symbols
    in an edge, shortening the depth of the trie."""

    def __init__(self):
        """Create an empty trie."""
        self._edges = {}  # a dictionary of first character: more characters, child node
        self._terminates = False

    def insert(self, token):
        """Insert token if not already in trie."""
        if not token:
            self._terminates = True
            return

        leader = token[:1]
        if token[:1] in self._edges:
            # an edge starts with the same character as this token
            token = token[1:]  # cut off first symbol
            more, child = self._edges[leader]
            if token.startswith(more):
                # the new token starts with the same run of characters as the current child there
                # i.e. edge is 'app', new token is 'apply'
                child.insert(token[len(more):])  # recurse down with 'ly'
            else:
                # there is only a partial match here, i.e. edge is 'apples', token is 'application'
                # cut the edge's label and insert a new node
                matched = _beginning_match(token, more)  # 4, the length of the common 'appl'
                our_more = more[:matched]  # shortened run for this node ('appl')
                new_edge = more[matched:]  # edge label for our current child in the new node ('es')
                # insert a new node between ourselves and the curent child there
                new_child = ShortTrie()
                self._edges[leader] = our_more, new_child  # 'appl' points to new node
                new_child._edges[new_edge[:1]] = new_edge[1:], child  # new node's 'es' edge points to the old child
                new_child.insert(token[matched:])  # insert 'ication' into the new node at 'appl'
        else:
            # no edges start with this token's first character, insert the whole thing with one edge
            child = ShortTrie()
            self._edges[token[:1]] = token[1:], child
            child._terminates = True

    def contains(self, token):
        """Return true if token is in trie."""
        if not token:
            return self._terminates
        elif token[:1] in self._edges:
            more, child = self._edges[token[:1]]
            token = token[1:]  # cut off first symbol
            if not token.startswith(more):
                return False  # does not fully match this edge
            return child.contains(token[len(more):])
        else:
            return False

    __contains__ = contains

    # noinspection PyProtectedMember
    def __iter__(self):
        """Traversing the short-trie depth-first."""
        stack = (None, None, None, None)  # singly linked list stack of loop context vars
        node = self
        prefix = None
        edge_items = iter(node._edges.items())  # iterator over the edges
        while node is not None:
            try:
                leader, (more, new_node) = next(edge_items)
            except StopIteration:
                stack, node, prefix, edge_items = stack
            else:
                stack = (stack, node, prefix, edge_items)
                node = new_node
                prefix = leader + more if prefix is None else prefix + leader + more
                edge_items = iter(node._edges.items())
                if node._terminates:
                    yield prefix

    # noinspection PyProtectedMember
    def breadth_first(self, prefix=None):
        """Helper breadth first traversal function for auto complete."""
        q = deque()
        q.appendleft((self, prefix))
        while q:
            node, prefix = q.pop()
            if node._terminates:
                yield prefix
            for leader, (more, child) in node._edges.items():
                edge = leader + more
                q.appendleft((child, edge if prefix is None else prefix + edge))

    def auto_complete(self, token, max_results=4):
        """Trie auto complete."""
        node = self
        prefix = token
        # traverse down until we have found the node that matches the given token
        while token:
            leader, token = token[:1], token[1:]
            if leader not in node._edges:
                return  # there are no entries with that next letter
            else:
                more, node = node._edges[leader]
                if not token.startswith(more):
                    return  # the whole edge isn't in the given token, either
                # cut off the rest of the edge label and continue
                token = token[len(more):]
        # iterate ovr the children breadth first from there
        # return default maximum of 4 tokens
        for item, _ in zip(node.breadth_first(prefix), range(max_results)):
            yield item
