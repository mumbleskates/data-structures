# coding=utf-8
from __future__ import unicode_literals
from builtins import open

import pytest

from data_structures.hash_table import HashTable


@pytest.fixture(scope='session')
def words():
    d = {}
    with open('test_data/words.txt', 'r') as f:
        for word in f:
            word = word.strip()
            if word not in d:
                d[word] = len(d)
    return d


def test_init():
    HashTable()


def test_non_string_key():
    ht = HashTable()
    with pytest.raises(TypeError):
        ht.set(6, 5)
    with pytest.raises(TypeError):
        ht.get(6)


def test_nonexistent_key():
    ht = HashTable()
    with pytest.raises(KeyError):
        ht.get('key')


def test_set_key_overwrite():
    ht = HashTable()
    ht.set('key', 1)
    assert ht.get('key') == 1
    ht.set('key', 2)
    assert ht.get('key') == 2


@pytest.mark.parametrize('n', range(5, 10))
def test_number_strings(n):
    ht = HashTable()
    ht.set(str(n), n)
    assert ht.get(str(n)) == n


def test_words(words):
    ht = HashTable()
    for k, v in words.items():
        ht.set(k, v)
    for k, v in words.items():
        assert ht.get(k) == v
