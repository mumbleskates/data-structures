# coding=utf-8
import pytest
import sys

from data_structures.simpleg import Graph


sys.setrecursionlimit(50000)


@pytest.fixture(scope='function')
def g():
    return Graph()


def test_nodes(g):
    assert set(g.nodes()) == set()
    for i in range(5):
        g.add_node(i)
    assert set(g.nodes()) == set(range(5))


def test_edges(g):
    assert set(g.edges()) == set()
    for i in range(5):
        g.add_edge(i, (i + 1) % 5)
    assert set(g.edges()) == {
        (i, (i + 1) % 5)
        for i in range(5)
    }


def test_add_node(g):
    g.add_node(1)
    assert g.nodes() == {1}
    # should not err
    g.add_node(1)


def test_add_edge(g):
    g.add_edge(1, 2)
    assert g.has_node(1)
    assert g.has_node(2)
    assert g.adjacent(1, 2)
    # should not err
    g.add_edge(1, 2)


def test_del_node(g):
    g.add_edge(1, 2)
    assert g.has_node(2)
    g.del_node(2)
    assert not g.has_node(2)
    with pytest.raises(KeyError):
        g.del_node(3)
    # check that dangling edge to 2 has been removed
    assert 2 not in g.neighbors(1)


def test_del_edge(g):
    g.add_edge(1, 2)
    assert g.adjacent(1, 2)
    g.del_edge(1, 2)
    assert not g.adjacent(1, 2)
    with pytest.raises(KeyError):
        g.del_edge(1, object())
    with pytest.raises(KeyError):
        g.del_edge(object(), 2)


def test_has_node(g):
    assert not g.has_node(1)
    g.add_node(1)
    assert g.has_node(1)


def test_neighbors(g):
    for i in range(5):
        g.add_node(i)
    for i in range(1, 5):
        g.add_edge(0, i)
    assert set(g.neighbors(0)) == set(range(1, 5))
    with pytest.raises(KeyError):
        g.neighbors(object())


def test_adjacent(g):
    g.add_node(0)
    g.add_edge(1, 2)
    assert g.adjacent(1, 2)
    assert not g.adjacent(1, 0)
    assert not g.adjacent(2, 1)
    with pytest.raises(KeyError):
        g.adjacent(1, object())
    with pytest.raises(KeyError):
        g.adjacent(object(), 2)


@pytest.fixture(scope='session')
def demo_graph():
    """
    Build a happy little tree graph:
          0
         / \
        1   2
       3 4 5 6
   """
    g = Graph()
    g.add_edge(0, 1)
    g.add_edge(1, 3)
    g.add_edge(1, 4)
    g.add_edge(0, 2)
    g.add_edge(2, 5)
    g.add_edge(2, 6)
    return g


@pytest.fixture(scope='session')
def demo_cycle_graph():
    """
    Build a happy little graph with a cycle:
       0 <==> 1
    """
    gc = Graph()
    gc.add_edge(0, 1)
    gc.add_edge(1, 0)
    return gc


DEPTH_FIRST_FUNCTIONS = [Graph.depth_first_traversal, Graph.recursive_depth_first]


@pytest.mark.parametrize("function", DEPTH_FIRST_FUNCTIONS)
def test_depth_first_traversal(demo_graph, function):
    """
    Test to make sure the tree is being traversed in depth first order
    """
    result = list(function(demo_graph, 0))
    assert result[0] == 0
    assert result[1] in [1, 2]
    assert result[2] in [3, 4, 5, 6]
    assert result[3] in [3, 4, 5, 6]
    assert result[4] in [1, 2]
    assert result[5] in [3, 4, 5, 6]
    assert result[6] in [3, 4, 5, 6]
    assert len(result) == 7


@pytest.mark.parametrize("function", DEPTH_FIRST_FUNCTIONS)
def test_depth_first_traverse_cycle(demo_cycle_graph, function):
    result_cycle = list(function(demo_cycle_graph, 0))
    assert result_cycle == [0, 1]


def test_breadth_first_traversal(demo_graph):
    """
    Test to make sure the tree is being traversed in breadth first order
    """
    result = list(demo_graph.breadth_first_traversal(0))
    assert result[0] == 0
    assert result[1] in [1, 2]
    assert result[2] in [1, 2]
    assert result[3] in [3, 4, 5, 6]
    assert result[4] in [3, 4, 5, 6]
    assert result[5] in [3, 4, 5, 6]
    assert result[6] in [3, 4, 5, 6]
    assert len(result) == 7


def test_breadth_first_traverse_cycle(demo_cycle_graph):
    result_cycle = list(demo_cycle_graph.breadth_first_traversal(0))
    assert result_cycle == [0, 1]


def _main():
    from functools import partial
    import json
    from timeit import timeit

    def traverse_all_depth_first(graph, start):
        for _ in graph.depth_first_traversal(start):
            pass

    def traverse_all_depth_first_recursive(graph, start):
        graph.recursive_depth_first(start)  # returns a list

    def traverse_all_breadth_first(graph, start):
        for _ in graph.breadth_first_traversal(start):
            pass

    def bench_performance():
        depth = timeit(partial(traverse_all_depth_first, g, start), number=100)
        breadth = timeit(partial(traverse_all_breadth_first, g, start), number=100)
        print("Depth first:           {}\n"
              "Breadth first:         {}\n"
              "    depth/breadth:           {}\n".format(depth, breadth, depth/breadth))

    def bench_recursion():
        stack = timeit(partial(traverse_all_depth_first, g, start), number=200)
        recurse = timeit(partial(traverse_all_depth_first_recursive, g, start), number=200)
        print("Non-recursive: {}\n"
              "Recursive:     {}\n"
              "Recursive/non: {}".format(stack, recurse, recurse/stack))

    print("Performance tests!")
    start = 0

    def make_branching_graph(size, factor):
        g = Graph()
        for parent in range(int(12000 / branch_factor + 1)):
            for child in (parent * branch_factor + 1 + x for x in range(branch_factor)):
                if child < 12000:
                    g.add_edge(parent, child)
        return g

    for branch_factor in [1, 2, 10]:
        print("12,000 nodes in a tree with branching factor {}".format(branch_factor))
        # build tree
        g = make_branching_graph(12000, branch_factor)
        bench_performance()
        print()

    print("~12000 nodes in a map-like graph:")
    # build graph
    g = Graph()
    with open("test_data/graph_data.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
    start = data['start']
    data = data['data']
    for edge in data:
        g.add_edge(edge['from'], edge['to'])

    bench_performance()
    print()

    all_connected_size = 300
    print("{} nodes all connected to each other:".format(all_connected_size))
    g = Graph()
    for i in range(all_connected_size):
        for j in range(all_connected_size):
            if i != j:
                g.add_edge(i, j)
    start = 0
    bench_performance()
    print()

    print("--- Recursion vs non-recursive stack ---")
    print("Comparison for all-connected graph:")
    bench_recursion()
    print()

    for branch_factor in [1, 2, 10]:
        print("With tree with 200 nodes, branching factor {}:".format(branch_factor))
        g = make_branching_graph(200, branch_factor)
        bench_recursion()
        print()


if __name__ == '__main__':
    _main()
