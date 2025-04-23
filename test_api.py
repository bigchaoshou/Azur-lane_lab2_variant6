import itertools
from hypothesis import given, strategies as st
from Binary_tree2 import (
    BinaryTreeDict,
    cons,
    empty,
    length,
    remove,
    member,
    to_list,
    from_list,
    concat,
    intersection,
    map_set,
    filter_set,
    reduce_set
)

    
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


keys = st.integers()
values = st.text()
key_value_pairs = st.tuples(keys, values)

# ------------------------- Basic Functionality Tests -------------------------
@given(pairs=st.lists(key_value_pairs))
def test_add_and_length(pairs):
    tree = empty()
    unique_keys = set()
    expected_length = 0
    for k, v in pairs:
        if k not in unique_keys:
            unique_keys.add(k)
            expected_length += 1
        tree = tree.add(k, v)
        assert len(tree.to_list()) == expected_length  # 使用 to_list() 长度替代 length()


@given(pairs=st.lists(key_value_pairs), key=st.integers())
def test_search(pairs, key):
    tree = from_list(pairs)
    # 预期值：最后一个出现的 key 对应的 value
    expected_value = next((v for k, v in reversed(pairs) if k == key), None)
    assert tree.search(key) == expected_value


@given(pairs=st.lists(key_value_pairs), key=st.integers(), new_value=st.text())
def test_add_overwrite(pairs, key, new_value):
    tree = from_list(pairs)
    updated_tree = tree.add(key, new_value)
    assert updated_tree.search(key) == new_value


# ------------------------- Remove & Member Tests -------------------------
@given(pairs=st.lists(key_value_pairs), key=st.integers())
def test_remove(pairs, key):
    tree = from_list(pairs)
    unique_keys = {k for k, _ in pairs}
    removed_tree = remove(tree, key)
    if key in unique_keys:
        assert not member(key, removed_tree)
        assert len(removed_tree.to_list()) == len(unique_keys) - 1
    else:
        assert removed_tree == tree  # 未修改原树


@given(pairs=st.lists(key_value_pairs), key=st.integers())
def test_member(pairs, key):
    tree = from_list(pairs)
    unique_keys = {k for k, _ in pairs}
    assert member(key, tree) == (key in unique_keys)


# ------------------------- List Conversion Tests -------------------------
@given(pairs=st.lists(key_value_pairs))
def test_from_list_to_list(pairs):
    tree = from_list(pairs)
    expected_dict = {}
    for k, v in pairs:
        expected_dict[k] = v
    expected = sorted(expected_dict.items(), key=lambda x: x[0])
    assert tree.to_list() == expected


# ------------------------- Higher-Order Functions Tests -------------------------
@given(pairs=st.lists(key_value_pairs))
def test_filter(pairs):
    tree = from_list(pairs)
    filtered = tree.filter(lambda k: k % 2 == 0)
    expected = [(k, v) for k, v in tree.to_list() if k % 2 == 0]
    assert filtered.to_list() == expected


@given(pairs=st.lists(key_value_pairs))
def test_map(pairs):
    tree = from_list(pairs)
    mapped = tree.map(lambda k: k + 1)
    expected = [(k + 1, v) for k, v in tree.to_list()]
    assert mapped.to_list() == sorted(expected, key=lambda x: x[0])


@given(pairs=st.lists(key_value_pairs))
def test_reduce(pairs):
    tree = from_list(pairs)
    sum_keys = tree.reduce(lambda acc, k: acc + k, 0)
    expected = sum(k for k, _ in tree.to_list())
    assert sum_keys == expected


# ------------------------- Iterator Test -------------------------
@given(pairs=st.lists(key_value_pairs))
def test_iterator(pairs):
    tree = from_list(pairs)
    via_iterator = list(iter(tree))
    assert sorted(via_iterator) == sorted(k for k, _ in tree.to_list())


# ------------------------- Empty Tree Test -------------------------
def test_empty():
    tree = empty()
    assert tree.is_empty()
    assert tree.to_list() == []


# ------------------------- Concatenation Tests -------------------------
@given(pairs1=st.lists(key_value_pairs), pairs2=st.lists(key_value_pairs))
def test_concat(pairs1, pairs2):
    t1 = from_list(pairs1)
    t2 = from_list(pairs2)
    combined = concat(t1, t2)
    expected_dict = dict(pairs1 + pairs2)
    expected = sorted(expected_dict.items(), key=lambda x: x[0])
    assert combined.to_list() == expected


@given(pairs1=st.lists(key_value_pairs), pairs2=st.lists(key_value_pairs), pairs3=st.lists(key_value_pairs))
def test_concat_associativity(pairs1, pairs2, pairs3):
    t1 = from_list(pairs1)
    t2 = from_list(pairs2)
    t3 = from_list(pairs3)
    # (t1 + t2) + t3
    left_assoc = concat(concat(t1, t2), t3)
    # t1 + (t2 + t3)
    right_assoc = concat(t1, concat(t2, t3))
    assert left_assoc == right_assoc


# ------------------------- Monoid Laws Test -------------------------
@given(pairs=st.lists(key_value_pairs))
def test_monoid_laws(pairs):
    t = from_list(pairs)
    empty_tree = empty()
    assert concat(empty_tree, t) == t
    assert concat(t, empty_tree) == t