"""Problem 2 - Binary search tree."""

# Programmed by CoolCat467

from __future__ import annotations

# Problem 2 - Binary search tree
# Copyright (C) 2026  CoolCat467
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

__title__ = "problem_2"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    Protocol,
    TypeVar,
)

if TYPE_CHECKING:
    from collections.abc import Generator, Iterable

T = TypeVar("T")


class SupportsLe(Protocol):
    """Protocol defining <= method."""

    def __le__(self, other: Any) -> bool: ...  # noqa: D105


C = TypeVar("C", bound=SupportsLe)


class Node(Generic[T]):
    """Node class.

    Keeps track of a value and an optional left and right node.
    """

    __slots__ = ("left", "right", "value")

    def __init__(
        self,
        value: T,
        left: Node[T] | None = None,
        right: Node[T] | None = None,
    ) -> None:
        """Initialize node."""
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        """Return representation of this class.

        Does not show left or right nodes directly to avoid infinite
        recursion.
        """
        extras = []
        if self.left is not None:
            extras.append("<left>")
        if self.right is not None:
            if not extras:
                extras.append("right=<right>")
            else:
                extras.append("<right>")
        extra = ", ".join(extras)
        if extra:
            extra = f", {extra}"
        return f"{self.__class__.__name__}({self.value!r}{extra})"

    @property
    def children(self) -> Generator[Node[T], None, None]:
        """Yield left and right child nodes if they exist."""
        if self.left is not None:
            yield self.left
        if self.right is not None:
            yield self.right

    def preorder(self) -> Generator[Node[T], None, None]:
        """Yield a preorder iteration of children."""
        yield self
        for child in self.children:
            yield from child.preorder()

    def inorder(self) -> Generator[Node[T], None, None]:
        """Yield a inorder iteration of children."""
        if self.left is not None:
            yield from self.left.inorder()
        yield self
        if self.right is not None:
            yield from self.right.inorder()

    def postorder(self) -> Generator[Node[T], None, None]:
        """Yield a postorder iteration of children."""
        for child in self.children:
            yield from child.preorder()
        yield self

    def render_tree_lines(self) -> list[str]:
        """Return list of lines from rendering tree."""
        # https://en.wikipedia.org/wiki/Box-drawing_characters was very
        # helpful writing this.
        lines = []
        lines.append(repr(self))
        children = tuple(self.children)
        for idx, child in enumerate(children):
            end = (idx + 1) == len(children)
            child_lines = iter(child.render_tree_lines())
            connect = "├└"[end]
            lines.append(f"{connect}{next(child_lines)}")
            child_connect = "│ "[end]
            for line in child_lines:
                lines.append(f"{child_connect}{line}")
        return lines

    def render_tree(self) -> str:
        """Return text representation of node connections."""
        return "\n".join(self.render_tree_lines())


def iterable_getitem(iterable: Iterable[T], index: int) -> T:
    """Return value at given index in iterable.

    Args:
        iterable (Iterable[T]): Iterable of T objects
        index (int): Number of steps to walk through iterable

    Returns:
        T object at given index in iterable.

    Raises:
        ValueError: if index negative or out of bounds.

    """
    if index < 0:
        raise IndexError
    for i, value in enumerate(iterable):
        if i == index:
            return value
    raise IndexError


class BinaryTree(Generic[C]):
    """Binary Tree class.

    Implements every required abstract method of
    `collections.abc.MutableSet`, though supports duplicate elements so
    not really a true set. No indexing support though so not a
    MutableSequence, and especially because order is not preserved.

    Every element you wish to store should be comparable with <= between
    all other element types you wish to store.
    """

    __slots__ = ("root",)

    def __init__(self, iterable: Iterable[C] | None = None) -> None:
        """Initialize from optional iterable.

        Args:
            iterable (Iterable[C] | None): Iterable object to initialize
            from. Values must be comparable with <=.

        """
        self.root: Node[C] | None = None

        if iterable is not None:
            self.update(iterable)

    def __iter__(self) -> Generator[C, None, None]:
        """Yield values from root inorder."""
        if self.root is None:
            return
        for node in self.root.inorder():
            yield node.value

    inorder = __iter__

    def preorder(self) -> Generator[C, None, None]:
        """Yield values from root preorder."""
        if self.root is None:
            return
        for node in self.root.preorder():
            yield node.value

    def postorder(self) -> Generator[C, None, None]:
        """Yield values from root postorder."""
        if self.root is None:
            return
        for node in self.root.postorder():
            yield node.value

    def __repr__(self) -> str:
        """Return representation of self."""
        items = ", ".join(map(repr, self))
        if items:
            items = f"({items})"
        return f"{self.__class__.__name__}({items})"

    def __len__(self) -> int:
        """Return number of elements."""
        if self.root is None:
            return 0

        count = 0
        for _node in self.root.inorder():
            count += 1
        return count

    def _find_node_position_prior(self, value: C) -> tuple[Node[C], Node[C]]:
        """Return prior and target node by searching tree for value.

        Args:
            value (C): Value to find prior and target node for.

        Returns:
            Tuple of (prior, target) where prior is the node just before
            the target node.

        Raises:
            KeyError: if tree is empty.

        """
        if self.root is None:
            raise KeyError

        current = prior = self.root
        next_node: Node[C] | None = current
        while next_node is not None:
            prior = current
            current = next_node
            if current.value <= value:
                next_node = current.left
            else:
                next_node = current.right

        return prior, current

    def _find_node_position(self, value: C) -> Node[C]:
        """Return target node by searching tree for value.

        Args:
            value (C): Value to find target node for.

        Returns:
            Target Node[C]

        Raises:
            KeyError: if tree is empty.

        """
        _prior, current = self._find_node_position_prior(value)

        return current

    def add(self, value: C) -> None:
        """Add a value to the tree."""
        if self.root is None:
            self.root = Node(value)
            return

        current = self._find_node_position(value)

        if current.value <= value:
            current.left = Node(value)
        else:
            current.right = Node(value)

    def update(self, iterable: Iterable[C]) -> None:
        """Extend tree by adding elements from the iterable."""
        for item in iterable:
            self.add(item)

    ##    def __ior__(self, rhs: object | Iterable[C]) -> Self:
    ##        """Self |= rhs."""
    ##        if not isinstance(rhs, Iterable):
    ##            return NotImplemented
    ##        self.update(rhs)
    ##        return self

    def remove(self, value: C) -> None:
        """Remove a value from the tree; it must be a member.

        If value is not a member, raise a KeyError.

        Args:
            value (C): Value to remove.

        Raises:
            KeyError: value is not a member of this tree.

        """
        prior, target = self._find_node_position_prior(value)

        if target.value != value:
            # print(f'{prior = }')
            # print(f'{target = }')
            raise KeyError

        # check if literally same object, not equality
        if target is prior.left:
            prior.left = None
        else:
            prior.right = None

        # add child nodes from removed item back on.
        # there is probably a smarter way to do this but it works.
        for child in target.children:
            # print(f'{child = }')
            self.update(node.value for node in child.inorder())

    def discard(self, value: C) -> None:
        """Remove an element from the tree if it is a member."""
        try:  # noqa: SIM105
            self.remove(value)
        except KeyError:
            pass

    def clear(self) -> None:
        """Remove all elements from the tree."""
        # because no backwards references in nodes, just killing root
        # reference should be fine.
        self.root = None

    def __contains__(self, value: C) -> bool:
        """Return bool(value in self)."""
        # works but slower than necessary
        ##for node in self.root.inorder():
        ##    if node.value == value:
        ##        return True
        # faster using the way the tree is organized
        current: Node[C] | None = self.root
        while current is not None:
            if current.value == value:
                return True
            if current.value <= value:  # noqa: SIM108
                current = current.left
            else:
                current = current.right
        return False

    def render(self) -> str:
        """Return string representation of internal node connections."""
        if self.root is None:
            return "<empty>"
        return self.root.render_tree()


def run() -> None:
    """Run program."""
    char_tree = BinaryTree("1234561245")
    print(f"{char_tree = }")
    print(char_tree.render())
    for value in char_tree:
        assert value in char_tree, f"{value!r} not in char_tree"
    # assuming "search" means `__contains__`?
    print(f'{"6" in char_tree = }')
    print()
    print("preorder:")
    print(" ".join(char_tree.preorder()))
    print()
    print("inorder:")
    print(" ".join(char_tree.inorder()))
    print()
    print("postorder:")
    print(" ".join(char_tree.postorder()))
    print()
    char_tree.remove("6")
    print(f"{char_tree = }")
    print(char_tree.render())
    print(f'{"6" in char_tree = }')
    print()
    char_tree.remove("5")
    print(f"{char_tree = }")
    print(char_tree.render())
    print()
    char_tree.remove("5")
    print(f"{char_tree = }")
    print(char_tree.render())
    print()
    char_tree.remove("2")
    print(f"{char_tree = }")
    print(char_tree.render())
    print()
    char_tree.add("0")
    print(f"{char_tree = }")
    print(char_tree.render())
    print()
    char_tree.clear()
    print(f"{char_tree = }")
    print(char_tree.render())


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
