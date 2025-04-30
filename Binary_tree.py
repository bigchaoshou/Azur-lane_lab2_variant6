from typing import (
    Optional, List, Tuple, Callable,
    Iterator, TypedDict, Generic, TypeVar, Iterable, Any
)

KT = TypeVar("KT",int,str,None)
VT = TypeVar('VT',int,str,None)
AccT = TypeVar('AccT')


def compare_keys(a: KT, b: KT) -> int:
    try:
        return (a > b) - (a < b)
    except TypeError:
        a_type = str(type(a))
        b_type = str(type(b))
        return (a_type > b_type) - (a_type < b_type)


class TreeNodeDict(TypedDict, total=False):
    key: int
    value: str
    left: Optional['TreeNodeDict']
    right: Optional['TreeNodeDict']


class BinaryTreeDict(Generic[KT, VT]):

    def __init__(self, root: Optional[TreeNodeDict] = None) -> None:
        self.root = root

    def is_empty(self) -> bool:
        return self.root is None

    def size(self) -> int:
        return self._size_recursive(self.root)

    def _size_recursive(self, node: Optional[TreeNodeDict]) -> int:
        if node is None:
            return 0
        return (1
                + self._size_recursive(node['left'])
                + self._size_recursive(node['right']))

    def add(self, key: KT, value: VT) -> 'BinaryTreeDict[KT, VT]':
        return BinaryTreeDict(self._add_recursive(self.root, key, value))

    def _add_recursive(
            self, node: Optional[TreeNodeDict],
            key: KT, value: VT) -> TreeNodeDict:
        if node is None:
            return {'key': key, 'value': value, 'left': None, 'right': None}

        cmp = compare_keys(key, node['key'])
        if cmp < 0:
            return {
                'key': node['key'],
                'value': node['value'],
                'left': self._add_recursive(node['left'], key, value),
                'right': node['right']
            }
        elif cmp > 0:
            return {
                'key': node['key'],
                'value': node['value'],
                'left': node['left'],
                'right': self._add_recursive(node['right'], key, value)
            }
        else:
            return {
                'key': key,
                'value': value,
                'left': node['left'],
                'right': node['right']
            }

    def search(self, key: KT) -> Optional[VT]:
        node = self._search_recursive(self.root, key)
        return node['value'] if node else None

    def _search_recursive(self,
                          node: Optional[TreeNodeDict],
                          key: KT) -> Optional[TreeNodeDict]:
        if node is None:
            return None
        cmp = compare_keys(key, node['key'])
        if cmp == 0:
            return node
        elif cmp < 0:
            return self._search_recursive(node['left'], key)
        else:
            return self._search_recursive(node['right'], key)

    def contains_key(self, key: KT) -> bool:
        return self._search_recursive(self.root, key) is not None

    def set_value(self, key: KT,
                  new_value: VT) -> 'BinaryTreeDict[KT, VT]':
        return self.add(key, new_value)

    def remove(self,
               key: KT) -> 'BinaryTreeDict[KT, VT]':
        return BinaryTreeDict(self._delete_recursive(self.root, key))

    def _delete_recursive(self,
                          node: Optional[TreeNodeDict],
                          key: KT) -> Optional[TreeNodeDict]:
        if node is None:
            return None

        cmp = compare_keys(key, node['key'])
        if cmp < 0:
            return {
                'key': node['key'],
                'value': node['value'],
                'left': self._delete_recursive(node['left'], key),
                'right': node['right']
            }
        elif cmp > 0:
            return {
                'key': node['key'],
                'value': node['value'],
                'left': node['left'],
                'right': self._delete_recursive(node['right'], key)
            }
        else:
            if node['left'] is None:
                return node['right']
            if node['right'] is None:
                return node['left']

            min_node = self._find_min(node['right'])
            return {
                'key': min_node['key'],
                'value': min_node['value'],
                'left': node['left'],
                'right': self._delete_recursive(node['right'], min_node['key'])
            }

    def _find_min(self, node: TreeNodeDict) -> TreeNodeDict:
        while node['left'] is not None:
            node = node['left']
        return node

    def contains_value(self, value: VT) -> bool:
        return self._value_recursive(self.root, value)

    def _value_recursive(self,
                         node: Optional[TreeNodeDict],
                         value: VT) -> bool:
        if node is None:
            return False
        return (
                node['value'] == value or
                self._value_recursive(node['left'], value) or
                self._value_recursive(node['right'], value)
        )

    @classmethod
    def from_list(cls,
                  lst: Iterable[Tuple[KT, VT]]
                  ) -> 'BinaryTreeDict[KT, VT]':
        bst = cls.empty()
        for key, value in lst:
            bst = bst.add(key, value)
        return bst

    def to_list(self) -> List[Tuple[KT, VT]]:
        result: List[Tuple[KT, VT]] = []
        self._inorder_traversal(self.root, result)
        return result

    def _inorder_traversal(self,
                           node: Optional[TreeNodeDict],
                           result: List[Tuple[KT, VT]]) -> None:
        if node is not None:
            self._inorder_traversal(node['left'], result)
            result.append((node['key'], node['value']))
            self._inorder_traversal(node['right'], result)

    def filter(self,
               predicate: Callable[[KT], bool]
               ) -> 'BinaryTreeDict[KT, VT]':
        result = [(k, v) for k, v in self.to_list() if predicate(k)]
        return BinaryTreeDict.from_list(result)

    def map(self, func: Callable[[KT], KT]) -> 'BinaryTreeDict[KT, VT]':
        new_tree: BinaryTreeDict[KT, VT] = BinaryTreeDict()
        for k, v in self.to_list():
            new_tree = new_tree.add(func(k), v)
        return new_tree

    def reduce(self, func: Callable[[AccT, KT], AccT], initial: AccT) -> AccT:
        result = initial
        for k, _ in self.to_list():
            result = func(result, k)
        return result

    def concat(self,
               other: 'BinaryTreeDict[KT, VT]'
               ) -> 'BinaryTreeDict[KT, VT]':
        new_tree = self
        for key in other:
            value = other.search(key)
            if value is not None:
                new_tree = new_tree.add(key, value)
        return new_tree

    def __iter__(self) -> Iterator[KT]:
        return (k for k, _ in self.to_list())

    def __str__(self) -> str:
        items = self.to_list()
        if not items:
            return "{}"
        return "{" + ", ".join(
            f"{repr(k)}: {repr(v)}" for k, v in items
        ) + "}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BinaryTreeDict):
            return False

        def inorder_gen(node):
            stack = []
            while stack or node:
                while node:
                    stack.append(node)
                    node = node["left"]
                node = stack.pop()
                yield (node["key"], node["value"])
                node = node["right"]

        gen1 = inorder_gen(self.root)
        gen2 = inorder_gen(other.root)

        for pair1, pair2 in zip(gen1, gen2):
            if pair1 != pair2:
                return False

        # Check if both trees had the same number of nodes
        try:
            next(gen1)
            return False
        except StopIteration:
            pass

        try:
            next(gen2)
            return False
        except StopIteration:
            pass

        return True

    @staticmethod
    def empty() -> 'BinaryTreeDict[KT, VT]':
        return BinaryTreeDict()


def empty() -> BinaryTreeDict[None, None]:
    return BinaryTreeDict.empty()


def cons(key: Any,
         value: Any,
         tree: BinaryTreeDict[Any, Any]) -> BinaryTreeDict[Any, Any]:
    return tree.add(key, value)


def concat(t1: BinaryTreeDict[Any, Any],
           t2: BinaryTreeDict[Any, Any]) -> BinaryTreeDict[Any, Any]:
    return t1.concat(t2)


def member(key: Any, tree: BinaryTreeDict[Any, Any]) -> bool:
    return tree.contains_key(key)


def remove(tree: BinaryTreeDict[Any, Any],
           key: Any) -> BinaryTreeDict[Any, Any]:
    return tree.remove(key)


def from_list(items: Iterable[Tuple[Any, Any]]
              ) -> BinaryTreeDict[Any, Any]:
    return BinaryTreeDict.from_list(items)


def to_list(tree: BinaryTreeDict[Any, Any]
            ) -> List[Tuple[Any, Any]]:
    return tree.to_list()


def length(tree: BinaryTreeDict[Any, Any]) -> int:
    return tree.size()


def intersection(t1: BinaryTreeDict[Any, Any],
                 t2: BinaryTreeDict[Any, Any]
                 ) -> BinaryTreeDict[Any, Any]:
    result = empty()
    for k, v in t1.to_list():
        if t2.contains_key(k):
            result = result.add(k, v)
    return result


def filter_set(tree: BinaryTreeDict[Any, Any],
               predicate: Callable[[Any], bool]
               ) -> BinaryTreeDict[Any, Any]:
    return tree.filter(predicate)


def map_set(tree: BinaryTreeDict[Any, Any],
            func: Callable[[Any],
            Tuple[Any, Any]]) -> BinaryTreeDict[Any, Any]:
    return tree.map(func)


def reduce_set(tree: BinaryTreeDict[Any, Any],
               func: Callable[[Any, Any], Any],
               initial: Any) -> Any:
    return tree.reduce(func, initial)
