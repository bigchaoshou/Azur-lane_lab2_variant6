from __future__ import annotations
from typing import Any, Callable, Generic, Iterator, Optional, Tuple, TypeVar, Union
from typing_extensions import Protocol

class SupportsRichComparison(Protocol):
    def __lt__(self, other: Any) -> bool: ...
    def __le__(self, other: Any) -> bool: ...
    def __gt__(self, other: Any) -> bool: ...
    def __ge__(self, other: Any) -> bool: ...

KT = TypeVar("KT", bound=SupportsRichComparison)
VT = TypeVar("VT")
AccT = TypeVar("AccT")

class BinaryTreeDict(Generic[KT, VT]):
    def __init__(self, node: Optional[dict] = None):
        if node is None:
            self.node = _EMPTY_NODE
        else:
            self.node = node

    def is_empty(self) -> bool:
        return self.node['key'] is None

    def add(self, key: KT, value: VT = None) -> BinaryTreeDict[KT, VT]:
        if self.is_empty():
            return BinaryTreeDict({'key': key, 'value': value, 'left': empty(), 'right': empty()})

        if key == self.node['key']:
            return BinaryTreeDict({
                'key': key,
                'value': value,
                'left': self.node['left'],
                'right': self.node['right']
            })
        elif key < self.node['key']:
            return BinaryTreeDict({
                'key': self.node['key'],
                'value': self.node['value'],
                'left': self.node['left'].add(key, value),
                'right': self.node['right']
            })
        else:
            return BinaryTreeDict({
                'key': self.node['key'],
                'value': self.node['value'],
                'left': self.node['left'],
                'right': self.node['right'].add(key, value)
            })

    def search(self, key: KT) -> Optional[VT]:
        if self.is_empty():
            return None
        if key == self.node['key']:
            return self.node['value']
        elif key < self.node['key']:
            return self.node['left'].search(key)
        else:
            return self.node['right'].search(key)

    def member(self, key: KT) -> bool:
        if self.is_empty():
            return False
        if key == self.node['key']:
            return True
        elif key < self.node['key']:
            return self.node['left'].member(key)
        else:
            return self.node['right'].member(key)

    def remove(self, key: KT) -> BinaryTreeDict[KT, VT]:
        if self.is_empty():
            return self
        if key < self.node['key']:
            new_left = self.node['left'].remove(key)
            return BinaryTreeDict({'key': self.node['key'], 'value': self.node['value'], 'left': new_left, 'right': self.node['right']})
        elif key > self.node['key']:
            new_right = self.node['right'].remove(key)
            return BinaryTreeDict({'key': self.node['key'], 'value': self.node['value'], 'left': self.node['left'], 'right': new_right})
        else:
            if self.node['left'].is_empty():
                return self.node['right']
            if self.node['right'].is_empty():
                return self.node['left']
            min_key, min_value = self.node['right']._find_min()
            new_right = self.node['right'].remove(min_key)
            return BinaryTreeDict({'key': min_key, 'value': min_value, 'left': self.node['left'], 'right': new_right})

    def _find_min(self) -> Tuple[KT, VT]:
        if self.node['left'].is_empty():
            return (self.node['key'], self.node['value'])
        return self.node['left']._find_min()

    def to_list(self) -> list[Tuple[KT, VT]]:
        if self.is_empty():
            return []
        return self.node['left'].to_list() + [(self.node['key'], self.node['value'])] + self.node['right'].to_list()

    @staticmethod
    def from_list(items: list[Tuple[KT, VT]]) -> BinaryTreeDict[KT, VT]:
        tree = empty()
        for k, v in items:
            tree = tree.add(k, v)
        return tree

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, BinaryTreeDict) and sorted(self.to_list()) == sorted(other.to_list())

    def __str__(self) -> str:
        return "{" + ", ".join(f"{repr(k)}: {repr(v)}" for k, v in sorted(self.to_list(), key=lambda x: (x[0] is not None, x[0]))) + "}"

    def __iter__(self) -> Iterator[KT]:
        for k, _ in self.to_list():
            yield k

    def map(self, f: Callable[[KT], KT]) -> BinaryTreeDict[KT, VT]:
        return BinaryTreeDict.from_list([(f(k), v) for k, v in self.to_list()])

    def filter(self, f: Callable[[KT], bool]) -> BinaryTreeDict[KT, VT]:
        return BinaryTreeDict.from_list([(k, v) for k, v in self.to_list() if f(k)])

    def reduce(self, f: Callable[[AccT, KT], AccT], acc: AccT) -> AccT:
        for k, _ in self.to_list():
            acc = f(acc, k)
        return acc


_EMPTY_NODE: dict = {'key': None, 'value': None, 'left': None, 'right': None}
_EMPTY_TREE: BinaryTreeDict = BinaryTreeDict(_EMPTY_NODE)
_EMPTY_NODE['left'] = _EMPTY_TREE
_EMPTY_NODE['right'] = _EMPTY_TREE

def empty() -> BinaryTreeDict[Any, Any]:
    return _EMPTY_TREE


def cons(key: KT, value: VT, tree: BinaryTreeDict[KT, VT]) -> BinaryTreeDict[KT, VT]:
    return tree.add(key, value)

def concat(t1: BinaryTreeDict[KT, VT], t2: BinaryTreeDict[KT, VT]) -> BinaryTreeDict[KT, VT]:
    return BinaryTreeDict.from_list(t1.to_list() + t2.to_list())

def length(tree: BinaryTreeDict[KT, VT]) -> int:
    return len(tree.to_list())

def member(key: KT, tree: BinaryTreeDict[KT, VT]) -> bool:
    return tree.member(key)

def remove(tree: BinaryTreeDict[KT, VT], key: KT) -> BinaryTreeDict[KT, VT]:
    return tree.remove(key)

def from_list(items: list[Tuple[KT, VT]]) -> BinaryTreeDict[KT, VT]:
    return BinaryTreeDict.from_list(items)

def to_list(tree: BinaryTreeDict[KT, VT]) -> list[Tuple[KT, VT]]:
    return tree.to_list()

def intersection(t1: BinaryTreeDict[KT, VT], t2: BinaryTreeDict[KT, VT]) -> BinaryTreeDict[KT, VT]:
    result = empty()
    for k, v in to_list(t1):
        if t2.member(k):
            result = result.add(k, v)
    return result


def map_set(tree: BinaryTreeDict[KT, None], f: Callable[[KT], KT]) -> BinaryTreeDict[KT, None]:
    return tree.map(f)

def filter_set(tree: BinaryTreeDict[KT, None], f: Callable[[KT], bool]) -> BinaryTreeDict[KT, None]:
    return tree.filter(f)

def reduce_set(tree: BinaryTreeDict[KT, None], f: Callable[[AccT, KT], AccT], acc: AccT) -> AccT:
    return tree.reduce(f, acc)
