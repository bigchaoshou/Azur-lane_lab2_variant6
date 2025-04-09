import itertools
from Binary_tree2 import *


def test_api():
    empty_tree = BinaryTreeDict()

    l1 = cons("none", "c", cons("two", "b",
                                cons("a", 1, empty_tree)))
    l2 = cons("a", 1, cons("none", "c",
                           cons("two", "b", empty_tree)))

    assert str(empty_tree) == "{}"
    assert str(l1) in [
        "{'a': 1, 'two': 'b', 'none': 'c'}",
        "{'a': 1, 'none': 'c', 'two': 'b'}",
        "{'two': 'b', 'a': 1, 'none': 'c'}",
        "{'two': 'b', 'none': 'c', 'a': 1}",
        "{'none': 'c', 'two': 'b', 'a': 1}",
        "{'none': 'c', 'a': 1, 'two': 'b'}",
    ]

    assert empty_tree != l1
    assert empty_tree != l2
    assert l1 == l2

    assert length(empty_tree) == 0
    assert length(l1) == 3
    assert length(l2) == 3

    assert (str(remove(l1, "none")) in
            ["{'two': 'b', 'a': 1}",
             "{'a': 1, 'two': 'b'}"])
    assert (str(remove(l1, "a")) in
            ["{'two': 'b', 'none': 'c'}",
            "{'none': 'c', 'two': 'b'}"])

    assert not member("none", empty_tree)
    assert member("none", l1)
    assert member("a", l1)
    assert member("two", l1)
    assert not member("three", l1)

    expected_pairs = [("a", 1), ("two", "b"), ("none", "c")]
    assert to_list(l1) in map(list, itertools.permutations(expected_pairs))

    assert l1 == from_list(expected_pairs)
    assert l1 == from_list([("two", "B"),
                            ("a", 1), ("two", "b"),
                            ("none", "c")])

    assert concat(l1, l2) == from_list([("two", "B"),
                                        ("a", 1), ("two", "b"),
                                        ("none", "c")])

    buf = []
    for e in l1:
        buf.append(e)
    assert buf in map(list, itertools.permutations(["a", "two", "none"]))

    lst = (list(map(lambda e: e[0], to_list(l1))) +
           list(map(lambda e: e[0], to_list(l2))))
    for e in l1:
        lst.remove(e)
    for e in l2:
        lst.remove(e)
    assert lst == []

    set1 = from_list([("a", None), ("b", None), ("c", None)])
    set2 = from_list([("b", None), ("c", None), ("d", None)])
    inter = intersection(set1, set2)
    assert to_list(inter) in map(list, itertools.permutations([("b", None),
                                                               ("c", None)]))

    mapped = map_set(set1, lambda k: k.upper())
    expected_keys = ["A", "B", "C"]
    assert sorted([k for k, _ in to_list(mapped)]) == expected_keys

    filtered = filter_set(set1, lambda k: 'b' in k)
    assert to_list(filtered) == [("b", None)]

    total_len = reduce_set(set1, lambda acc, k: acc + len(k), 0)
    assert total_len == len("a") + len("b") + len("c")
