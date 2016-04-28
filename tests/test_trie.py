# -*- coding: utf -8 -*-
from builtins import open

import mock
import pytest

from data_structures.trie import Trie, ShortTrie

# inspector doesn't see this otherwise
mock.patch.object = mock.patch.object


def _words():
    with open('test_data/words.txt', 'r') as f:
        return set(word.strip() for word in f)
words = list(_words())[:5000]


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


@pytest.mark.parametrize('trie_type', (Trie, ShortTrie))
def test_iteration(trie_type):
    trie = trie_type()
    for word in words:
        trie.insert(word)
    iterated = list(trie)
    unique_iterated = set(iterated)
    assert len(iterated) == len(unique_iterated)
    assert unique_iterated == set(words)


@pytest.mark.parametrize('trie_type', (Trie, ShortTrie))
def test_iteration_empty(trie_type):
    trie = trie_type()
    assert list(trie) == []


@pytest.mark.parametrize('trie_type', (Trie, ShortTrie))
def test_breadth_first(trie_type):
    trie = trie_type()
    for item in [
        "abc",
        "abcdef",
        "abcdefghi",
        "abcdef456",
        "abc123",
        "abc123ghi",
        "abc123456",
    ]:
        trie.insert(item)
    breadth = list(trie.breadth_first())
    assert len(breadth) == 7
    middle = ["abcdef", "abc123"]
    bottom = ["abcdefghi", "abcdef456", "abc123ghi", "abc123456"]
    assert breadth[0] == "abc"
    assert all(item in middle for item in breadth[1:3])
    assert all(item in bottom for item in breadth[3:])


@pytest.mark.parametrize('trie_type', (Trie, ShortTrie))
@pytest.mark.parametrize('prefix', ["", "prefix_"])
def test_breadth_first_many(trie_type, prefix):
    trie = trie_type()
    for word in words:
        trie.insert(word)
    iterated = list(trie.breadth_first(prefix=prefix))
    unique_iterated = set(iterated)
    assert len(iterated) == len(unique_iterated)
    assert unique_iterated == set(prefix + word for word in words)


AUTOCOMPLETE_DATA = [
    (['a', 'ab', 'abc', 'abcd', 'aardvark', 'asdffasg', 'asdf', 'bsdf', 'absolutel', '5'], 'a'),
    (['a', 'ab', 'abc', 'abcd', 'aardvark', 'asdffasg', 'asdf', 'bsdf', 'absolutel', '5'], 'as'),
    (['a', 'ab', 'abc', 'abcd', 'aardvark', 'asdffasg', 'asdf', 'bsdf', 'absolutel', '5'], ''),
    ([], 'something'),
]


@pytest.mark.parametrize('trie_type', (Trie, ShortTrie))
@pytest.mark.parametrize('items, token', AUTOCOMPLETE_DATA)
@pytest.mark.parametrize('limit', [0, 1, 4, 1000000000])
def test_autocomplete(trie_type, items, token, limit):
    trie = trie_type()
    for item in items:
        trie.insert(item)
    autocompleted = list(trie.auto_complete(token, max_results=limit))
    assert len(autocompleted) <= limit
    assert all(auto.startswith(token) for auto in autocompleted)
