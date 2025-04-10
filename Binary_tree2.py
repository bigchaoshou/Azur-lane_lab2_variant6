from __future__ import annotations
from typing import Any, Callable, Iterator, Optional, Tuple
from typing_extensions import TypedDict


class TreeNodeDict(TypedDict, total=False):
    key: int
    value: str
    left: Optional['TreeNodeDict']
    right: Optional['TreeNodeDict']


class BinaryTreeDict:
    def __init__(self, node: Optional[TreeNodeDict] = None):
        if node is None:
            node = {'key': None, 'value': None, 'left': empty(), 'right': empty()}
        self.node = node

    def is_empty(self) -> bool:
        return self.node['key'] is None

    def add(self, key: int, value: str) -> BinaryTreeDict[int, str]:
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

    def search(self, key: int) -> Optional[str]:
        """Search for the value corresponding to the key (immutable)"""
        if self.is_empty():
            return None
        if key == self.node['key']:
            return self.node['value']
        elif key < self.node['key']:
            return self.node['left'].search(key)
        else:
            return self.node['right'].search(key)

    def member(self, key: int) -> bool:
        """Check if the key is in the tree"""
        return self.search(key) is not None

    def remove(self, key: int) -> BinaryTreeDict[int, str]:
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

    def _find_min(self) -> Tuple[int, str]:
        """Find the minimum key-value pair in the tree"""
        if self.node['left'].is_empty():
            return (self.node['key'], self.node['value'])
        return self.node['left']._find_min()

    def to_list(self) -> list[Tuple[int, str]]:
        """Convert the tree to a sorted list of key-value pairs"""
        if self.is_empty():
            return []
        return self.node['left'].to_list() + [(self.node['key'], self.node['value'])] + self.node['right'].to_list()

    @staticmethod
    def from_list(items: list[Tuple[int, str]]) -> BinaryTreeDict[int, str]:
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

    def __iter__(self) -> Iterator[int]:
        """Iterator for the keys in the tree"""
        for k, _ in self.to_list():
            yield k

    def map(self, f: Callable[[int, str], Tuple[int, str]]) -> BinaryTreeDict[int, str]:
        """Apply a function to each key-value pair (immutable operation)"""
        return BinaryTreeDict.from_list([f(k, v) for k, v in self.to_list()])

    def filter(self, f: Callable[[int, str], bool]) -> BinaryTreeDict[int, str]:
        """Filter the tree by a predicate (immutable operation)"""
        return BinaryTreeDict.from_list([(k, v) for k, v in self.to_list() if f(k, v)])

    def reduce(self, f: Callable[[str, int, str], str], acc: str) -> str:
        """Fold the tree with an accumulator (immutable operation)"""
        for k, v in self.to_list():
            acc = f(acc, k, v)
        return acc


def empty() -> BinaryTreeDict[Any, Any]:
    """Create an empty tree"""
    return BinaryTreeDict({'key': None, 'value': None, 'left': None, 'right': None})


def cons(key: int, value: str, tree: BinaryTreeDict[int, str]) -> BinaryTreeDict[int, str]:
    """Add a key-value pair to the tree (immutable)"""
    return tree.add(key, value)


def concat(t1: BinaryTreeDict[int, str], t2: BinaryTreeDict[int, str]) -> BinaryTreeDict[int, str]:
    """Concatenate two trees into a new one (immutable)"""
    return BinaryTreeDict.from_list(t1.to_list() + t2.to_list())


def length(tree: BinaryTreeDict[int, str]) -> int:
    """Get the length of the tree (immutable)"""
    return len(tree.to_list())


def member(key: int, tree: BinaryTreeDict[int, str]) -> bool:
    """Check if a key is in the tree (immutable)"""
    return tree.member(key)


def remove(tree: BinaryTreeDict[int, str], key: int) -> BinaryTreeDict[int, str]:
    """Remove a key-value pair from the tree (immutable)"""
    return tree.remove(key)


def from_list(items: list[Tuple[int, str]]) -> BinaryTreeDict[int, str]:
    """Create a tree from a list of key-value pairs (immutable)"""
    return BinaryTreeDict.from_list(items)


def to_list(tree: BinaryTreeDict[int, str]) -> list[Tuple[int, str]]:
    """Convert the tree to a list of key-value pairs (immutable)"""
    return tree.to_list()


def intersection(t1: BinaryTreeDict[int, str], t2: BinaryTreeDict[int, str]) \
        -> BinaryTreeDict[int, str]:
    result = empty()
    for k, v in to_list(t1):
        if t2.member(k):
            result = result.add(k, v)
    return result


def map_set(tree: BinaryTreeDict[int, None], f: Callable[[int], int]) \
        -> BinaryTreeDict[int, None]:
    return tree.map(f)


def filter_set(tree: BinaryTreeDict[int, None], f: Callable[[int], bool]) \
        -> BinaryTreeDict[int, None]:
    return tree.filter(f)


def reduce_set(tree: BinaryTreeDict[int, None], f: Callable[[str, int], str],
               acc: str) -> str:
    return tree.reduce(f, acc)
