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
            node = {'key': None, 'value': None, 'left': empty(), 'right': empty()}
        self.node = node

    def is_empty(self) -> bool:
        return self.node['key'] is None

    def add(self, key: KT, value: VT) -> BinaryTreeDict[KT, VT]:
        """Add a new key-value pair to the tree (immutable operation)"""
        if self.is_empty():
            return BinaryTreeDict({'key': key, 'value': value, 'left': empty(), 'right': empty()})

        if key == self.node['key']:
            return BinaryTreeDict({'key': key, 'value': value, 'left': self.node['left'], 'right': self.node['right']})
        elif key < self.node['key']:
            new_left = self.node['left'].add(key, value)  # Recursively create new left subtree
            return BinaryTreeDict(
                {'key': self.node['key'], 'value': self.node['value'], 'left': new_left, 'right': self.node['right']})
        else:
            new_right = self.node['right'].add(key, value)  # Recursively create new right subtree
            return BinaryTreeDict(
                {'key': self.node['key'], 'value': self.node['value'], 'left': self.node['left'], 'right': new_right})

    def search(self, key: KT) -> Optional[VT]:
        """Search for the value corresponding to the key (immutable)"""
        if self.is_empty():
            return None
        if key == self.node['key']:
            return self.node['value']
        elif key < self.node['key']:
            return self.node['left'].search(key)
        else:
            return self.node['right'].search(key)

    def member(self, key: KT) -> bool:
        """Check if the key is in the tree"""
        return self.search(key) is not None

    def remove(self, key: KT) -> BinaryTreeDict[KT, VT]:
        """Remove a key-value pair (immutable operation)"""
        if self.is_empty():
            return self
        if key < self.node['key']:
            new_left = self.node['left'].remove(key)  # Recursively create new left subtree
            return BinaryTreeDict(
                {'key': self.node['key'], 'value': self.node['value'], 'left': new_left, 'right': self.node['right']})
        elif key > self.node['key']:
            new_right = self.node['right'].remove(key)  # Recursively create new right subtree
            return BinaryTreeDict(
                {'key': self.node['key'], 'value': self.node['value'], 'left': self.node['left'], 'right': new_right})
        else:
            # Node to be deleted
            if self.node['left'].is_empty():
                return self.node['right']  # Return right subtree
            if self.node['right'].is_empty():
                return self.node['left']  # Return left subtree
            min_key, min_value = self.node['right']._find_min()
            new_right = self.node['right'].remove(min_key)  # Recursively remove min node from right subtree
            return BinaryTreeDict({'key': min_key, 'value': min_value, 'left': self.node['left'], 'right': new_right})

    def _find_min(self) -> Tuple[KT, VT]:
        """Find the minimum key-value pair in the tree"""
        if self.node['left'].is_empty():
            return (self.node['key'], self.node['value'])
        return self.node['left']._find_min()

    def to_list(self) -> list[Tuple[KT, VT]]:
        """Convert the tree to a sorted list of key-value pairs"""
        if self.is_empty():
            return []
        return self.node['left'].to_list() + [(self.node['key'], self.node['value'])] + self.node['right'].to_list()

    @staticmethod
    def from_list(items: list[Tuple[KT, VT]]) -> BinaryTreeDict[KT, VT]:
        """Create a tree from a list of key-value pairs"""
        tree = empty()
        for k, v in items:
            tree = tree.add(k, v)
        return tree

    def __eq__(self, other: Any) -> bool:
        """Check if two trees are equal"""
        return isinstance(other, BinaryTreeDict) and self.to_list() == other.to_list()

    def __str__(self) -> str:
        """String representation of the tree"""
        return "{" + ", ".join(f"{repr(k)}: {repr(v)}" for k, v in self.to_list()) + "}"

    def __iter__(self) -> Iterator[KT]:
        """Iterator for the keys in the tree"""
        for k, _ in self.to_list():
            yield k

    def map(self, f: Callable[[KT, VT], Tuple[KT, VT]]) -> BinaryTreeDict[KT, VT]:
        """Apply a function to each key-value pair (immutable operation)"""
        return BinaryTreeDict.from_list([f(k, v) for k, v in self.to_list()])

    def filter(self, f: Callable[[KT, VT], bool]) -> BinaryTreeDict[KT, VT]:
        """Filter the tree by a predicate (immutable operation)"""
        return BinaryTreeDict.from_list([(k, v) for k, v in self.to_list() if f(k, v)])

    def reduce(self, f: Callable[[AccT, KT, VT], AccT], acc: AccT) -> AccT:
        """Fold the tree with an accumulator (immutable operation)"""
        for k, v in self.to_list():
            acc = f(acc, k, v)
        return acc


def empty() -> BinaryTreeDict[Any, Any]:
    """Create an empty tree"""
    return BinaryTreeDict()


def cons(key: KT, value: VT, tree: BinaryTreeDict[KT, VT]) -> BinaryTreeDict[KT, VT]:
    """Add a key-value pair to the tree (immutable)"""
    return tree.add(key, value)


def concat(t1: BinaryTreeDict[KT, VT], t2: BinaryTreeDict[KT, VT]) -> BinaryTreeDict[KT, VT]:
    """Concatenate two trees into a new one (immutable)"""
    return BinaryTreeDict.from_list(t1.to_list() + t2.to_list())


def length(tree: BinaryTreeDict[KT, VT]) -> int:
    """Get the length of the tree (immutable)"""
    return len(tree.to_list())


def member(key: KT, tree: BinaryTreeDict[KT, VT]) -> bool:
    """Check if a key is in the tree (immutable)"""
    return tree.member(key)


def remove(tree: BinaryTreeDict[KT, VT], key: KT) -> BinaryTreeDict[KT, VT]:
    """Remove a key-value pair from the tree (immutable)"""
    return tree.remove(key)


def from_list(items: list[Tuple[KT, VT]]) -> BinaryTreeDict[KT, VT]:
    """Create a tree from a list of key-value pairs (immutable)"""
    return BinaryTreeDict.from_list(items)


def to_list(tree: BinaryTreeDict[KT, VT]) -> list[Tuple[KT, VT]]:
    """Convert the tree to a list of key-value pairs (immutable)"""
    return tree.to_list()
