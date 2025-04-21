from typing import Optional, List, Tuple, Callable, Iterator, TypedDict


class TreeNodeDict(TypedDict, total=False):
    key: int
    value: str
    left: Optional['TreeNodeDict']
    right: Optional['TreeNodeDict']


class BSTDictionary:
    def __init__(self, root: Optional[TreeNodeDict] = None) -> None:
        self.root = root

    def size(self) -> int:
        return self._size_recursive(self.root)

    def _size_recursive(self, node: Optional[TreeNodeDict]) -> int:
        if node is None:
            return 0
        return 1 + self._size_recursive(node['left']) + self._size_recursive(node['right'])

    def add(self, key: int, value: str) -> 'BSTDictionary':
        return BSTDictionary(self._add_recursive(self.root, key, value))

    def _add_recursive(self, node: Optional[TreeNodeDict], key: int, value: str) -> TreeNodeDict:
        if node is None:
            return {'key': key, 'value': value, 'left': None, 'right': None}
        if key < node['key']:
            return {
                'key': node['key'],
                'value': node['value'],
                'left': self._add_recursive(node['left'], key, value),
                'right': node['right']
            }
        elif key > node['key']:
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

    def search(self, key: int) -> Optional[str]:
        node = self._search_recursive(self.root, key)
        return node['value'] if node else None

    def _search_recursive(self, node: Optional[TreeNodeDict], key: int) -> Optional[TreeNodeDict]:
        if node is None or node['key'] == key:
            return node
        elif key < node['key']:
            return self._search_recursive(node['left'], key)
        else:
            return self._search_recursive(node['right'], key)

    def set(self, key: int, new_value: str) -> 'BSTDictionary':
        return self.add(key, new_value)

    def remove(self, key: int) -> 'BSTDictionary':
        return BSTDictionary(self._delete_recursive(self.root, key))

    def _delete_recursive(self, node: Optional[TreeNodeDict], key: int) -> Optional[TreeNodeDict]:
        if node is None:
            return None
        if key < node['key']:
            return {
                'key': node['key'],
                'value': node['value'],
                'left': self._delete_recursive(node['left'], key),
                'right': node['right']
            }
        elif key > node['key']:
            return {
                'key': node['key'],
                'value': node['value'],
                'left': node['left'],
                'right': self._delete_recursive(node['right'], key)
            }
        else:
            if node['left'] is None:
                return node['right']
            elif node['right'] is None:
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

    def member(self, value: str) -> bool:
        return self._member_recursive(self.root, value)

    def _member_recursive(self, node: Optional[TreeNodeDict], value: str) -> bool:
        if node is None:
            return False
        if node['value'] == value:
            return True
        return self._member_recursive(node['left'], value) or self._member_recursive(node['right'], value)

    def reverse(self) -> List[Tuple[int, str]]:
        return list(reversed(self.to_list()))

    @classmethod
    def from_list(cls, lst: List[Tuple[int, str]]) -> 'BSTDictionary':
        bst = cls.empty()
        for key, value in lst:
            bst = bst.add(key, value)
        return bst

    def to_list(self) -> List[Tuple[int, str]]:
        result: List[Tuple[int, str]] = []
        self._inorder_traversal(self.root, result)
        return result

    def _inorder_traversal(self, node: Optional[TreeNodeDict], result: List[Tuple[int, str]]) -> None:
        if node is not None:
            self._inorder_traversal(node['left'], result)
            result.append((node['key'], node['value']))
            self._inorder_traversal(node['right'], result)

    def filter(self, predicate: Callable[[int, str], bool]) -> 'BSTDictionary':
        result = [(k, v) for k, v in self.to_list() if predicate(k, v)]
        return BSTDictionary.from_list(result)

    def map(self, func: Callable[[int, str], Tuple[int, str]]) -> 'BSTDictionary':
        mapped = [func(k, v) for k, v in self.to_list()]
        return BSTDictionary.from_list(mapped)

    def reduce(self, func: Callable[[str, int, str], str], initial_value: str) -> str:
        result = initial_value
        for k, v in self.to_list():
            result = func(result, k, v)
        return result

    def __iter__(self) -> Iterator[Tuple[int, str]]:
        return iter(self.to_list())

    @staticmethod
    def empty() -> 'BSTDictionary':
        return BSTDictionary()

    def concat(self, other: 'BSTDictionary') -> 'BSTDictionary':
        result = self
        for key, value in other:
            result = result.add(key, value)
        return result
