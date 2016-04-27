# -*- coding: utf -8 -*-
import mock
import pytest

from data_structures.trie import Trie

# inspector doesn't see this otherwise
mock.patch.object = mock.patch.object


def _words():
    with open('test_data/words.txt', 'r') as f:
        return set(word.strip() for word in f)
words = list(_words())


class UsageCounter(object):
    def __init__(self):
        self.count = 0

    def wrap(self, function):
        """Decorator to count usages of a function"""
        def dec(*args, **kwargs):
            self.count += 1
            function(*args, **kwargs)
        return dec


def test_init():
    Trie()


def test_insert():
    for word in words:
        trie = Trie()
        trie.insert(word)
        assert trie.contains(word)


OVERLAPPING_WORD_SETS = [
    ['apple', 'application'],
    ['a', 'ab', 'abc', 'abcd', 'afeijf'],
    ['ab', 'abc'],
    words,
]


@pytest.mark.parametrize('values', OVERLAPPING_WORD_SETS)
def test_values_overlap(values):
    counter = UsageCounter()
    # count the number of Trie objects that get initialized
    with mock.patch.object(Trie, "__init__", counter.wrap(Trie.__init__)):
        trie = Trie()
        total_length = 0
        for word in values:
            trie.insert(word)
            total_length += len(word)
    # there should be fewer nodes in our trie than there were letters in the words
    assert total_length > counter.count


def test_contains_empty():
    trie = Trie()
    assert '' not in trie


def test_contains():
    half = len(words) >> 1
    words_a = words[:half]
    words_b = words[half:]

    trie = Trie()
    for word in words_a:
        trie.insert(word)

    for word in words_a:
        assert word in trie
    for word in words_b:
        assert word not in trie
