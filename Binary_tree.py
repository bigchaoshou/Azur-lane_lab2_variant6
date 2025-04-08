from typing import Any, Optional, List, Tuple, Callable, TypeVar, Iterator

K = TypeVar('K')
V = TypeVar('V')
T = TypeVar('T')

class BSTDictionary:
    def __init__(self) -> None:
        self.root: Optional[dict] = None
        self._size: int = 0

    def size(self) -> int:
        return self._size

    def add(self, key: K, value: V) -> None:
        if self.root is None:
            self.root = {'key': key, 'value': value, 'left': None, 'right': None}
            self._size += 1
        else:
            if self._add_recursive(self.root, key, value):
                self._size += 1

    def _add_recursive(self, node: dict, key: K, value: V) -> bool:
        if key < node['key']:
            if node['left'] is None:
                node['left'] = {'key': key, 'value': value, 'left': None, 'right': None}
                return True
            else:
                return self._add_recursive(node['left'], key, value)
        elif key > node['key']:
            if node['right'] is None:
                node['right'] = {'key': key, 'value': value, 'left': None, 'right': None}
                return True
            else:
                return self._add_recursive(node['right'], key, value)
        else:
            node['value'] = value
            return False

    def _find_min(self, node: dict) -> dict:
        while node['left'] is not None:
            node = node['left']
        return node

    def search(self, key: K) -> Optional[V]:
        node = self._search_recursive(self.root, key)
        return node['value'] if node else None

    def _search_recursive(self, node: Optional[dict], key: K) -> Optional[dict]:
        if node is None or node['key'] == key:
            return node
        elif key < node['key']:
            return self._search_recursive(node['left'], key)
        else:
            return self._search_recursive(node['right'], key)

    def set(self, key: K, new_value: V) -> None:
        node = self._search_recursive(self.root, key)
        if node:
            node['value'] = new_value

    def remove(self, key: K) -> None:
        if self.search(key) is not None:
            self.root = self._delete_recursive(self.root, key)
            self._size -= 1

    def _delete_recursive(self, node: Optional[dict], key: K) -> Optional[dict]:
        if node is None:
            return node
        if key < node['key']:
            node['left'] = self._delete_recursive(node['left'], key)
        elif key > node['key']:
            node['right'] = self._delete_recursive(node['right'], key)
        else:
            if node['left'] is None:
                return node['right']
            elif node['right'] is None:
                return node['left']
            temp = self._find_min(node['right'])
            node['key'], node['value'] = temp['key'], temp['value']
            node['right'] = self._delete_recursive(node['right'], temp['key'])
        return node

    def member(self, value: V) -> bool:
        return self._member_recursive(self.root, value)

    def _member_recursive(self, node: Optional[dict], value: V) -> bool:
        if node is None:
            return False
        if node['value'] == value:
            return True
        return (self._member_recursive(node['left'], value) or
                self._member_recursive(node['right'], value))

    def reverse(self) -> List[Tuple[K, V]]:
        result: List[Tuple[K, V]] = []
        self._inorder_traversal(self.root, result)
        return result[::-1]

    @classmethod
    def from_list(cls, lst: List[Tuple[K, V]]) -> 'BSTDictionary':
        bst_dict = cls()
        for key, value in lst:
            bst_dict.add(key, value)
        return bst_dict

    def to_list(self) -> List[Tuple[K, V]]:
        result: List[Tuple[K, V]] = []
        self._inorder_traversal(self.root, result)
        return result

    def _inorder_traversal(self, node: Optional[dict], result: List[Tuple[K, V]]) -> None:
        if node is not None:
            self._inorder_traversal(node['left'], result)
            result.append((node['key'], node['value']))
            self._inorder_traversal(node['right'], result)

    def filter(self, predicate: Callable[[K, V], bool]) -> List[Tuple[K, V]]:
        result: List[Tuple[K, V]] = []
        self._filter_recursive(self.root, predicate, result)
        return sorted(result, key=lambda x: x[0])

    def _filter_recursive(self, node: Optional[dict],
                         predicate: Callable[[K, V], bool],
                         result: List[Tuple[K, V]]) -> None:
        if node:
            if predicate(node['key'], node['value']):
                result.append((node['key'], node['value']))
            self._filter_recursive(node['left'], predicate, result)
            self._filter_recursive(node['right'], predicate, result)

    def map(self, func: Callable[[K, V], Tuple[K, V]]) -> List[Tuple[K, V]]:
        result: List[Tuple[K, V]] = []
        self._map_recursive(self.root, func, result)
        return BSTDictionary.from_list(result).to_list()

    def _map_recursive(self, node: Optional[dict],
                      func: Callable[[K, V], Tuple[K, V]],
                      result: List[Tuple[K, V]]) -> None:
        if node:
            result.append(func(node['key'], node['value']))
            self._map_recursive(node['left'], func, result)
            self._map_recursive(node['right'], func, result)

    def reduce(self, func: Callable[[T, K, V], T], initial_value: T) -> T:
        return self._reduce_recursive(self.root, func, initial_value)

    def _reduce_recursive(self, node: Optional[dict],
                         func: Callable[[T, K, V], T],
                         value: T) -> T:
        if node is None:
            return value
        value = self._reduce_recursive(node['left'], func, value)
        value = func(value, node['key'], node['value'])
        value = self._reduce_recursive(node['right'], func, value)
        return value

    def __iter__(self) -> Iterator[Tuple[K, V]]:
        self._iter_stack: List[dict] = []
        self._push_left(self.root)
        return self

    def __next__(self) -> Tuple[K, V]:
        if not self._iter_stack:
            raise StopIteration
        node = self._iter_stack.pop()
        self._push_left(node['right'])
        return node['key'], node['value']

    def _push_left(self, node: Optional[dict]) -> None:
        while node:
            self._iter_stack.append(node)
            node = node['left']

    @staticmethod
    def empty() -> 'BSTDictionary':
        return BSTDictionary()

    def concat(self, other: 'BSTDictionary') -> 'BSTDictionary':
        if not isinstance(other, BSTDictionary) or other.root is None:
            return self  # 如果另一个字典为空或不是 BSTDictionary，直接返回当前字典

        # 定义一个递归的添加方法，将另一个字典的节点添加到当前字典中
        def add_other_tree(node: Optional[dict]) -> None:
            if node is not None:
                self.add(node['key'], node['value'])  # 直接调用 add 方法将节点添加到当前树
                add_other_tree(node['left'])  # 递归添加左子树
                add_other_tree(node['right'])  # 递归添加右子树

        # 将另一个字典的树中的节点添加到当前树
        add_other_tree(other.root)
        return self  # 返回当前字典（修改后的字典）
