from typing import (
    Optional, List, Tuple, Callable,
    Iterator, TypedDict, Generic, TypeVar, Iterable, Any
)
import itertools

# 定义类型变量
KT = TypeVar('KT', int, str, None)  # 键类型允许int、str、None
VT = TypeVar('VT')  # 值类型完全泛型
AccT = TypeVar('AccT')  # 累加器类型泛型


def compare_keys(a: KT, b: KT) -> int:
    """自定义键比较函数，处理None、int、str类型的比较"""
    if a is None:
        if b is None:
            return 0
        else:
            return -1  # None < 非None
    elif b is None:
        return 1  # 非None > None
    elif isinstance(a, int) and isinstance(b, int):
        return (a > b) - (a < b)
    elif isinstance(a, int) and isinstance(b, str):
        return -1  # int < str
    elif isinstance(a, str) and isinstance(b, int):
        return 1  # str > int
    elif isinstance(a, str) and isinstance(b, str):
        return (a > b) - (a < b)
    else:
        raise ValueError(f"Unsupported key types: {type(a)} and {type(b)}")


class TreeNodeDict(TypedDict, total=False):
    """二叉搜索树节点字典结构"""
    key: KT
    value: VT
    left: Optional['TreeNodeDict']
    right: Optional['TreeNodeDict']


class BinaryTreeDict(Generic[KT, VT]):
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

    def add(self, key: KT, value: VT) -> 'BinaryTreeDict[KT, VT]':
        """添加/更新键值对，返回新字典"""
        return BinaryTreeDict(self._add_recursive(self.root, key, value))

    def _add_recursive(self, node: Optional[TreeNodeDict], key: KT, value: VT) -> TreeNodeDict:
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
        """搜索指定键的值"""
        node = self._search_recursive(self.root, key)
        return node['value'] if node else None

    def _search_recursive(self, node: Optional[TreeNodeDict], key: KT) -> Optional[TreeNodeDict]:
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
        """检查键是否存在"""
        return self._search_recursive(self.root, key) is not None

    def set_value(self, key: KT, new_value: VT) -> 'BinaryTreeDict[KT, VT]':
        """更新键对应的值，返回新字典"""
        return self.add(key, new_value)

    def remove(self, key: KT) -> 'BinaryTreeDict[KT, VT]':
        """删除指定键的条目，返回新字典"""
        return BinaryTreeDict(self._delete_recursive(self.root, key))

    def _delete_recursive(self, node: Optional[TreeNodeDict], key: KT) -> Optional[TreeNodeDict]:
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

    def contains_value(self, value: VT) -> bool:
        """检查值是否存在"""
        return self._value_recursive(self.root, value)

    def _value_recursive(self, node: Optional[TreeNodeDict], value: VT) -> bool:
        if node is None:
            return False
        return (
                node['value'] == value or
                self._value_recursive(node['left'], value) or
                self._value_recursive(node['right'], value)
        )

    @classmethod
    def from_list(cls, lst: Iterable[Tuple[KT, VT]]) -> 'BinaryTreeDict[KT, VT]':
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

    def filter(self, predicate: Callable[[KT, VT], bool]
               ) -> 'BinaryTreeDict[KT, VT]':
        """过滤键值对生成新字典"""
        result = [(k, v) for k, v in self.to_list() if predicate(k, v)]
        return BinaryTreeDict.from_list(result)

    def map(self, func: Callable[[KT, VT], Tuple[KT, VT]]) -> 'BinaryTreeDict[KT, VT]':
        """映射键值对生成新字典"""
        mapped = [func(k, v) for k, v in self.to_list()]
        return BinaryTreeDict.from_list(mapped)

    def reduce(self, func: Callable[[AccT, KT, VT], AccT], initial: AccT) -> AccT:
        """归约操作"""
        result = initial
        for k, v in self.to_list():
            result = func(result, k, v)
        return result

    def concat(self, other: 'BinaryTreeDict[KT, VT]') -> 'BinaryTreeDict[KT, VT]':
        """合并两个字典"""
        new_tree = self
        for key, value in other:
            new_tree = new_tree.add(key, value)
        return new_tree

    def __iter__(self) -> Iterator[KT]:
        """迭代器支持（返回键）"""
        return (k for k, v in self.to_list())

    def __str__(self) -> str:
        """字典的字符串表示"""
        items = self.to_list()
        if not items:
            return "{}"
        return "{" + ", ".join(f"{repr(k)}: {repr(v)}" for k, v in items) + "}"

    def __eq__(self, other: object) -> bool:
        """判断两个字典是否相等"""
        if not isinstance(other, BinaryTreeDict):
            return False
        return self.to_list() == other.to_list()

    @staticmethod
    def empty() -> 'BinaryTreeDict[KT, VT]':
        """创建空字典"""
        return BinaryTreeDict()


# ------------------------------
# 全局辅助函数（适配测试用例）
# ------------------------------

def empty() -> BinaryTreeDict[None, None]:
    return BinaryTreeDict.empty()


def cons(key: Any, value: Any, tree: BinaryTreeDict[Any, Any]) -> BinaryTreeDict[Any, Any]:
    return tree.add(key, value)


def concat(t1: BinaryTreeDict[Any, Any], t2: BinaryTreeDict[Any, Any]) -> BinaryTreeDict[Any, Any]:
    return t1.concat(t2)


def member(key: Any, tree: BinaryTreeDict[Any, Any]) -> bool:
    return tree.contains_key(key)


def remove(tree: BinaryTreeDict[Any, Any], key: Any) -> BinaryTreeDict[Any, Any]:
    return tree.remove(key)


def from_list(items: Iterable[Tuple[Any, Any]]) -> BinaryTreeDict[Any, Any]:
    return BinaryTreeDict.from_list(items)


def to_list(tree: BinaryTreeDict[Any, Any]) -> List[Tuple[Any, Any]]:
    return tree.to_list()


def length(tree: BinaryTreeDict[Any, Any]) -> int:
    return tree.size()


def intersection(t1: BinaryTreeDict[Any, Any], t2: BinaryTreeDict[Any, Any]) -> BinaryTreeDict[Any, Any]:
    result = empty()
    for k, v in t1.to_list():
        if t2.contains_key(k):
            result = result.add(k, v)
    return result


def filter(tree: BinaryTreeDict[Any, Any], predicate: Callable[[Any, Any], bool]) -> BinaryTreeDict[Any, Any]:
    return tree.filter(predicate)


def map(tree: BinaryTreeDict[Any, Any], func: Callable[[Any, Any], Tuple[Any, Any]]) -> BinaryTreeDict[Any, Any]:
    return tree.map(func)


def reduce(tree: BinaryTreeDict[Any, Any], func: Callable[[Any, Any, Any], Any], initial: Any) -> Any:
    return tree.reduce(func, initial)