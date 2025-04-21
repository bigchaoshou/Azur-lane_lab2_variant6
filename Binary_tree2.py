from typing import (
    Optional, List, Tuple, Callable,
    Iterator, TypedDict, Generic, TypeVar, Iterable
)

# 定义类型变量
KT = TypeVar('KT', int, None)  # 键类型仅允许int
VT = TypeVar('VT', str, None)  # 值类型完全泛型
AccT = TypeVar('AccT', int, None)  # 累加器类型泛型


class TreeNodeDict(TypedDict, total=False):
    """二叉搜索树节点字典结构"""
    key: KT
    value: VT
    left: Optional['TreeNodeDict']
    right: Optional['TreeNodeDict']


class BSTDictionary(Generic[KT, VT]):
    """不可变二叉搜索树字典"""

    def __init__(self, root: Optional[TreeNodeDict] = None) -> None:
        self.root = root

    def size(self) -> int:
        """获取字典条目数"""
        return self._size_recursive(self.root)

    def _size_recursive(self, node: Optional[TreeNodeDict]) -> int:
        if node is None:
            return 0
        return 1 + self._size_recursive(node['left']) + self._size_recursive(node['right'])

    def add(self, key: KT, value: VT) -> 'BSTDictionary[KT, VT]':
        """添加/更新键值对，返回新字典"""
        return BSTDictionary(self._add_recursive(self.root, key, value))

    def _add_recursive(self, node: Optional[TreeNodeDict], key: KT, value: VT) -> TreeNodeDict:
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

    def search(self, key: KT) -> Optional[VT]:
        """搜索指定键的值"""
        node = self._search_recursive(self.root, key)
        return node['value'] if node else None

    def _search_recursive(self, node: Optional[TreeNodeDict], key: KT) -> Optional[TreeNodeDict]:
        if node is None or node['key'] == key:
            return node
        return self._search_recursive(node['left'], key) if key < node['key'] else self._search_recursive(node['right'],
                                                                                                          key)

    def set_value(self, key: KT, new_value: VT) -> 'BSTDictionary[KT, VT]':
        """更新键对应的值，返回新字典"""
        return self.add(key, new_value)

    def remove(self, key: KT) -> 'BSTDictionary[KT, VT]':
        """删除指定键的条目，返回新字典"""
        return BSTDictionary(self._delete_recursive(self.root, key))

    def _delete_recursive(self, node: Optional[TreeNodeDict], key: KT) -> Optional[TreeNodeDict]:
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
            if node['right'] is None:
                return node['left']

            # 找到右子树最小节点
            min_node = self._find_min(node['right'])
            return {
                'key': min_node['key'],
                'value': min_node['value'],
                'left': node['left'],
                'right': self._delete_recursive(node['right'], min_node['key'])
            }

    def _find_min(self, node: TreeNodeDict) -> TreeNodeDict:
        """查找子树最小节点"""
        while node['left'] is not None:
            node = node['left']
        return node

    def member(self, value: VT) -> bool:
        """检查值是否存在"""
        return self._member_recursive(self.root, value)

    def _member_recursive(self, node: Optional[TreeNodeDict], value: VT) -> bool:
        if node is None:
            return False
        return (
                node['value'] == value or
                self._member_recursive(node['left'], value) or
                self._member_recursive(node['right'], value)
        )

    @classmethod
    def from_list(cls, lst: Iterable[Tuple[KT, VT]]) -> 'BSTDictionary[KT, VT]':
        """从可迭代对象创建字典"""
        bst = cls.empty()
        for key, value in lst:
            bst = bst.add(key, value)
        return bst

    def to_list(self) -> List[Tuple[KT, VT]]:
        """转换为有序键值对列表"""
        result: List[Tuple[KT, VT]] = []
        self._inorder_traversal(self.root, result)
        return result

    def _inorder_traversal(self, node: Optional[TreeNodeDict], result: List[Tuple[KT, VT]]) -> None:
        if node is not None:
            self._inorder_traversal(node['left'], result)
            result.append((node['key'], node['value']))
            self._inorder_traversal(node['right'], result)

    def filter(self, predicate: Callable[[KT, VT], bool]) -> 'BSTDictionary[KT, VT]':
        result = [(k, v) for k, v in self.to_list() if predicate(k, v)]
        return BSTDictionary.from_list(result)

    def map(self, func: Callable[[KT, VT], Tuple[KT, VT]]) -> 'BSTDictionary[KT, VT]':
        """映射键值对生成新字典"""
        mapped = [func(k, v) for k, v in self.to_list()]
        return BSTDictionary.from_list(mapped)

    def reduce(self, func: Callable[[AccT, KT, VT], AccT], initial: AccT) -> AccT:
        """归约操作"""
        result = initial
        for k, v in self.to_list():
            result = func(result, k, v)
        return result

    def concat(self, other: 'BSTDictionary[KT, VT]') -> 'BSTDictionary[KT, VT]':
        """合并两个字典"""
        new_tree = self
        for key, value in other:
            new_tree = new_tree.add(key, value)
        return new_tree

    def __iter__(self) -> Iterator[Tuple[KT, VT]]:
        """迭代器支持"""
        return iter(self.to_list())

    @staticmethod
    def empty() -> 'BSTDictionary[KT, VT]':
        """创建空字典"""
        return BSTDictionary()


# 全局辅助函数
def empty() -> BSTDictionary[int, str]:
    """创建空字典（键类型为int，值类型为str）"""
    return BSTDictionary.empty()


def cons(key: int, value: str, tree: BSTDictionary[int, str]) -> BSTDictionary[int, str]:
    """添加键值对"""
    return tree.add(key, value)


def concat(t1: BSTDictionary[int, str], t2: BSTDictionary[int, str]) -> BSTDictionary[int, str]:
    """合并两个字典"""
    return t1.concat(t2)


def member(value: str, tree: BSTDictionary[int, str]) -> bool:
    """检查值是否存在"""
    return tree.member(value)


def remove(tree: BSTDictionary[int, str], key: int) -> BSTDictionary[int, str]:
    """删除指定键"""
    return tree.remove(key)


def intersection(t1: BSTDictionary[int, str], t2: BSTDictionary[int, str]) -> BSTDictionary[int, str]:
    """获取键交集字典"""
    result = empty()
    for k, v in t1.to_list():
        if t2.search(k) is not None:
            result = result.add(k, v)
    return result


def from_list(items: Iterable[Tuple[int, str]]) -> BSTDictionary[int, str]:
    """从列表创建字典"""
    return BSTDictionary.from_list(items)


def to_list(tree: BSTDictionary[int, str]) -> List[Tuple[int, str]]:
    """转换为列表"""
    return tree.to_list()


def map_func(tree: BSTDictionary[int, str], func: Callable[[int, str], Tuple[int, str]]) -> BSTDictionary[int, str]:
    """映射操作"""
    return tree.map(func)


def filter_func(tree: BSTDictionary[int, str], predicate: Callable[[int, str], bool]) -> BSTDictionary[int, str]:
    """过滤操作"""
    return tree.filter(predicate)


def reduce_func(tree: BSTDictionary[int, str], func: Callable[[AccT, int, str], AccT], initial: AccT) -> AccT:
    """归约操作"""
    return tree.reduce(func, initial)


def size(tree: BSTDictionary[int, str]) -> int:
    """获取字典大小"""
    return tree.size()