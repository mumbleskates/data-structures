# -*- coding: utf-8 -*-



TEST_SET = {
    [],
    [1],
    [2, 3, 4],
    "abc",
}

@pytest.mark.parameterize("items", TEST_SET)
def test_append(items):
    from dll import Dll
    t_dll = Dll()
    t_dll.append(items)
    assert list(t_dll) == list(items)


def test_insert():
    pass