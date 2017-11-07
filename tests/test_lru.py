# coding=utf-8
from __future__ import unicode_literals
from builtins import range, str

import pytest

from data_structures.lru import Lru


def test_works_as_dict():
    lru = Lru()
    default = object()
    for i in range(10):
        assert lru.current_cost == len(lru) == i
        assert i not in lru
        lru[i] = str(i)
        assert i in lru
    assert lru.current_cost == len(lru) == 10
    for i in range(10):
        assert lru[i] == str(i)
        assert lru.get(i, default) == str(i)
    assert 999 not in lru
    assert lru.get(999, default) is default


def test_del():
    lru = Lru((i, i) for i in range(10))
    del lru[5]
    assert 5 not in lru
    assert lru.current_cost == len(lru) == 9
    assert set(lru.keys()) == set(range(10)) - {5}
    assert list(lru.items()) == [(i, i) for i in range(10) if i != 5]
    with pytest.raises(KeyError):
        del lru[5]


def test_bump():
    lru = Lru((i, i) for i in range(3))
    assert list(lru.items()) == [(0, 0), (1, 1), (2, 2)]
    assert lru[1] == 1
    assert list(lru.items()) == [(0, 0), (2, 2), (1, 1)]
    lru[0] = 'what'
    assert list(lru.items()) == [(2, 2), (1, 1), (0, 'what')]


def test_evicts_least_recent():
    lru = Lru(budget=5)
    for i in range(10):
        lru[i] = str(i)
        assert set(lru.keys()) == set(range(i - 4, i + 1)) & set(range(10))


def test_access_refreshes_recency():
    lru = Lru(budget=10)
    for i in range(10):
        lru[i] = str(i)
    assert lru[0] == '0'  # refresh recency of 0
    lru[10] = '10'
    assert set(lru.keys()) == set(range(11)) - {1}  # 1 was evicted
    lru[2] = 'two'  # refresh recency of 2
    lru[1] = 'one'  # re-add 1, which was evicted
    assert set(lru.keys()) == set(range(11)) - {3}  # 3 was evicted


def test_custom_cost():
    lru = Lru(budget=10, cost_func=(lambda k, v: k))
    for i in range(7):
        lru[i] = str(i)
        assert lru.current_cost == sum(lru.keys())
        assert lru.current_cost <= 10
    assert set(lru.keys()) == {6}  # only this key should remain
    # over-budget items should be discarded immediately
    lru[100] = 'this will be discarded'
    assert set(lru.keys()) == {6}


def test_items():
    lru = Lru(budget=5)
    for i in range(10):
        lru[i] = str(i)
        assert set(lru) == {k for k, v in lru.items()}
    items = list(lru.items())
    assert items == [(i, str(i)) for i in range(5, 10)]
    lru2 = Lru(items)
    assert list(lru2.items()) == items


def test_force_positive_budget():
    with pytest.raises(ValueError):
        Lru(budget=-100)
    lru = Lru(budget=0)
    assert lru.budget == 0
    lru.budget = 5
    assert lru.budget == 5
    with pytest.raises(ValueError):
        lru.budget = -100
    assert lru.budget == 5


def test_lowering_budget_evicts():
    lru = Lru((i, i) for i in range(10))
    assert set(lru.keys()) == set(range(10))
    lru.budget = 5
    assert set(lru.keys()) == set(range(5, 10))
    assert lru.current_cost == len(lru) == lru.budget == 5
    lru.budget = 10
    assert lru.current_cost == len(lru) == 5
    assert lru.budget == 10
    lru[10] = 10
    assert lru.current_cost == 6
    assert set(lru.keys()) == set(range(5, 11))


def test_cost_numeric_stability():
    lru = Lru()
    lru['small'] = 1e-100
    lru['big'] = 1e100
    demonstrate = lru['small'] + lru['big']
    demonstrate -= lru['big']
    demonstrate -= lru['small']
    assert demonstrate != 0
    del lru['big']
    del lru['small']
    assert lru.current_cost == 0
