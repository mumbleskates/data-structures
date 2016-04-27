# -*- coding: utf -8 -*-
import mock
import pytest

from data_structures.trie import Trie, ShortTrie

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


@pytest.mark.parametrize('trie_type', (Trie, ShortTrie))
def test_init(trie_type):
    trie_type()


@pytest.mark.parametrize('trie_type', (Trie, ShortTrie))
def test_insert(trie_type):
    for word in words:
        trie = trie_type()
        trie.insert(word)
        assert trie.contains(word)


OVERLAPPING_WORD_SETS = [
    ['apple', 'application'],
    ['a', 'ab', 'abc', 'abcd', 'afeijf'],
    ['ab', 'abc'],
    words,
]


@pytest.mark.parametrize('trie_type', (Trie, ShortTrie))
@pytest.mark.parametrize('values', OVERLAPPING_WORD_SETS)
def test_values_overlap(values, trie_type):
    counter = UsageCounter()
    # count the number of Trie objects that get initialized
    with mock.patch.object(trie_type, "__init__", counter.wrap(trie_type.__init__)):
        trie = trie_type()
        total_length = 0
        for word in values:
            trie.insert(word)
            total_length += len(word)
    # there should be fewer nodes in our trie than there were letters in the words
    assert total_length > counter.count


SHORTENABLE = [
    ["a longish string"],
    ["a sentence split part", "a sentence split partway through"],
    ["abcdefg", "abcdefghijklmnop", "abcdefghijklmnopqrstuvwxy", "abcdefghijklmnopqrstuvwxyz"],
]


@pytest.mark.parametrize('values', SHORTENABLE)
def test_tree_shortens(values):
    counter = UsageCounter()
    # count the number of Trie objects that get initialized
    with mock.patch.object(ShortTrie, "__init__", counter.wrap(ShortTrie.__init__)):
        trie = ShortTrie()
        for value in values:
            trie.insert(value)
    assert counter.count == 1 + len(values)


@pytest.mark.parametrize('trie_type', (Trie, ShortTrie))
def test_contains_empty(trie_type):
    trie = trie_type()
    assert '' not in trie


@pytest.mark.parametrize('trie_type', (Trie, ShortTrie))
def test_contains(trie_type):
    half = len(words) >> 1
    words_a = words[:half]
    words_b = words[half:]

    trie = trie_type()
    for word in words_a:
        trie.insert(word)

    for word in words_a:
        assert word in trie
    for word in words_b:
        assert word not in trie
