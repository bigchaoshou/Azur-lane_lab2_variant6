from __future__ import annotations
from typing import Any, Callable, Iterator, Optional, Tuple, Union
from typing_extensions import TypedDict
import itertools


class TreeNodeDict(TypedDict, total=False):
    key: str
    value: Any
    left: Optional['TreeNodeDict']
    right: Optional['TreeNodeDict']


class BinaryTreeDict:
    def __init__(self, node: Optional[TreeNodeDict] = None):
        if node is None:
            node = {'key': None, 'value': None, 'left': empty(), 'right': empty()}
        self.node = node

    def is_empty(self) -> bool:
        return self.node['key'] is None

    def add(self, key: str, value: Any) -> BinaryTreeDict:
        if self.is_empty():
            return BinaryTreeDict({'key': key, 'value': value, 'left': empty(), 'right': empty()})
        if key == self.node['key']:
            return BinaryTreeDict({'key': key, 'value': value, 'left': self.node['left'], 'right': self.node['right']})
        elif key < self.node['key']:
            new_left = self.node['left'].add(key, value)
            return BinaryTreeDict({'key': self.node['key'], 'value': self.node['value'], 'left': new_left, 'right': self.node['right']})
        else:
            new_right = self.node['right'].add(key, value)
            return BinaryTreeDict({'key': self.node['key'], 'value': self.node['value'], 'left': self.node['left'], 'right': new_right})

    def search(self, key: str) -> Optional[Any]:
        if self.is_empty():
            return None
        if key == self.node['key']:
            return self.node['value']
        elif key < self.node['key']:
            return self.node['left'].search(key)
        else:
            return self.node['right'].search(key)

    def member(self, key: str) -> bool:
        if self.is_empty():
            return False
        if key == self.node['key']:
            return True
        elif key < self.node['key']:
            return self.node['left'].member(key)
        else:
            return self.node['right'].member(key)

    def remove(self, key: str) -> BinaryTreeDict:
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

    def _find_min(self) -> Tuple[str, Any]:
        if self.node['left'].is_empty():
            return (self.node['key'], self.node['value'])
        return self.node['left']._find_min()

    def to_list(self) -> list[Tuple[str, Any]]:
        if self.is_empty():
            return []
        return self.node['left'].to_list() + [(self.node['key'], self.node['value'])] + self.node['right'].to_list()

    @staticmethod
    def from_list(items: list[Tuple[str, Any]]) -> BinaryTreeDict:
        tree = empty()
        for k, v in items:
            tree = tree.add(k, v)
        return tree

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, BinaryTreeDict) and self.to_list() == other.to_list()

    def __str__(self) -> str:
        return "{" + ", ".join(f"{repr(k)}: {repr(v)}" for k, v in self.to_list()) + "}"

    def __iter__(self) -> Iterator[str]:
        for k, _ in self.to_list():
            yield k

    def map(self, f: Callable[[str, Any], Tuple[str, Any]]) -> BinaryTreeDict:
        return BinaryTreeDict.from_list([f(k, v) for k, v in self.to_list()])

    def filter(self, f: Callable[[str, Any], bool]) -> BinaryTreeDict:
        return BinaryTreeDict.from_list([(k, v) for k, v in self.to_list() if f(k, v)])

    def reduce(self, f: Callable[[str, str, Any], str], acc: str) -> str:
        for k, v in self.to_list():
            acc = f(acc, k, v)
        return acc


def empty() -> BinaryTreeDict:
    return BinaryTreeDict({'key': None, 'value': None, 'left': None, 'right': None})


def intersection(t1: BinaryTreeDict, t2: BinaryTreeDict) -> BinaryTreeDict:
    result = empty()
    for k, v in t1.to_list():
        if t2.member(k):
            result = result.add(k, v)
    return result


def cons(key: str, value: Any, tree: BinaryTreeDict) -> BinaryTreeDict:
    return tree.add(key, value)


def map_set(tree: BinaryTreeDict, f: Callable[[str], str]) -> BinaryTreeDict:
    return tree.map(lambda k, v: (f(k), v))


def filter_set(tree: BinaryTreeDict, f: Callable[[str], bool]) -> BinaryTreeDict:
    return tree.filter(lambda k, v: f(k))


def reduce_set(tree: BinaryTreeDict, f: Callable[[Any, str, Any], Any], acc: Any) -> Any:
    return tree.reduce(f, acc)
