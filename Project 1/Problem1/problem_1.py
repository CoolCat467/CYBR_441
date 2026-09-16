"""Problem 1 - Student class & Deque."""

# Programmed by CoolCat467

from __future__ import annotations

# Problem 1 - Student class & Deque
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

__title__ = "problem_1"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from collections.abc import Generator, Iterable
from typing import TYPE_CHECKING, Generic, TypeVar, cast, overload

if TYPE_CHECKING:
    from typing_extensions import Self

T = TypeVar("T")


class Student:
    """Student class.

    Keeps track of name, age, and GPA."""

    __slots__ = ("_age", "_gpa", "_name")

    def __init__(self, name: str, age: int, gpa: float) -> None:
        """Initialize student."""
        self.set_name(name)
        self.set_age(age)
        self.set_gpa(gpa)

    def set_name(self, name: str) -> None:
        """Set `name` field."""
        self._name = name

    def set_age(self, age: int) -> None:
        """Set `age` field."""
        self._age = age

    def set_gpa(self, gpa: float) -> None:
        """Set `gpa` field."""
        self._gpa = gpa

    def get_name(self) -> str:
        """Return `name` field."""
        return self._name

    def get_age(self) -> int:
        """Return `age` field."""
        return self._age

    def get_gpa(self) -> float:
        """Return `gpa` field."""
        return self._gpa

    def __repr__(self) -> str:
        """Return representation of this instance."""
        return f"{self.__class__.__name__}({self.get_name()!r}, {self.get_age()!r}, {self.get_gpa()!r})"

    def __eq__(self, rhs: object) -> bool:
        """Return if self == rhs and treat string comparison as name comparison."""
        if isinstance(rhs, str):
            return self.get_name() == rhs
        if not isinstance(rhs, self.__class__):
            return False
        return (
            self.get_name() == rhs.get_name()
            and self.get_age() == rhs.get_age()
            and self.get_gpa() == rhs.get_gpa()
        )


class Node(Generic[T]):
    """Node class.

    Keeps track of a value and an optional next and prior node."""

    __slots__ = ("next", "prior", "value")

    def __init__(
        self,
        value: T,
        next_: Node[T] | None = None,
        prior: Node[T] | None = None,
    ) -> None:
        """Initialize node."""
        self.value = value
        self.next = next_
        self.prior = prior

    def __repr__(self) -> str:
        """Return representation of this class.

        Does not show next or prior nodes directly to avoid infinite
        recursion."""
        extras = []
        if self.next is not None:
            extras.append("<next>")
        if self.prior is not None:
            if not extras:
                extras.append("prior=<prior>")
            else:
                extras.append("<prior>")
        extra = ", ".join(extras)
        if extra:
            extra = f", {extra}"
        return f"{self.__class__.__name__}({self.value!r}{extra})"


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


class Deque(Generic[T]):
    """Doubly-linked list.

    Implements everything needed to be treated the same as a
    collections.abc.MutableSequence except `.sort`
    """

    __slots__ = ("head", "tail")

    def __init__(self, iterable: Iterable[T] | None = None) -> None:
        """Initialize from optional iterable.

        Args:
            iterable (Iterable[T] | None): Iterable object to initialize
            from.
        """
        self.head: Node[T] | None = None
        self.tail: Node[T] | None = None

        if iterable is not None:
            self.extend(iterable)

    def _iter_nodes_gen(self) -> Generator[Node[T], None, None]:
        """Yield nodes from head to tail."""
        current = self.head
        while current is not None:
            yield current
            current = current.next

    def _iter_nodes_tail_gen(self) -> Generator[Node[T], None, None]:
        """Yield nodes from tail to head."""
        current = self.tail
        while current is not None:
            yield current
            current = current.prior

    def __iter__(self) -> Generator[T, None, None]:
        """Yield values from head to tail."""
        for node in self._iter_nodes_gen():
            yield node.value

    def __reversed__(self) -> Generator[T, None, None]:
        """Return a reverse iterator over the deque.

        Yield values from tail to head.
        """
        for node in self._iter_nodes_tail_gen():
            yield node.value

    def __len__(self) -> int:
        """Return number of elements."""
        if self.head is None:
            return 0

        assert self.tail is not None

        count = 1
        current: Node[T] | None = self.head

        while current != self.tail:
            assert current is not None
            current = current.next
            count += 1
        return count

    def _node_getitem(self, index: int) -> Node[T]:
        """Return node at given index.

        Args:
            index (int): Index to get node from.

        Returns:
            Node object at given index.

        Raises:
            IndexError: When index out of bounds.
        """
        if self.head is None or self.tail is None:
            raise IndexError
        if index >= 0:
            return iterable_getitem(self._iter_nodes_gen(), index)
        return iterable_getitem(self._iter_nodes_tail_gen(), -(index + 1))

    @overload
    def __getitem__(self, index: int, /) -> T: ...
    @overload
    def __getitem__(
        self,
        index: slice[int | None, int | None, int | None],
        /,
    ) -> Self: ...

    def __getitem__(
        self,
        index: int | slice[int | None, int | None, int | None],
        /,
    ) -> T | Self:
        """Return value at given index.

        Args:
            index (int | slice[int | None, int | None, int | None]):
            Integer index or slice indices to get value(s) from.

        Returns:
            T value at int index or new Deque of T values from slice.

        Raises:
            IndexError: Invalid index.
        """
        if isinstance(index, slice):
            return self._getitem_slice(index)
        return self._node_getitem(index).value

    def _getitem_slice(
        self,
        slice_: slice[int | None, int | None, int | None],
    ) -> Self:
        """Return deque of slice elements.

        Args:
            slice_ (slice[int | None, int | None, int | None]): Slice
            object to get index values from.

        Returns:
            New Deque from slice index values.
        """
        slice_range = range(*slice_.indices(len(self)))
        return self.__class__(self[x] for x in slice_range)

    @overload
    def __setitem__(self, index: int, value: T, /) -> None: ...
    @overload
    def __setitem__(
        self,
        index: slice[int | None, int | None, int | None],
        value: Iterable[T],
        /,
    ) -> None: ...

    def __setitem__(
        self,
        index: int | slice[int | None, int | None, int | None],
        value: T | Iterable[T],
        /,
    ) -> None:
        """Set self[index] to value.

        Args:
            index (int | slice[int | None, int | None, int | None]):
                Integer index or slice indices to set value(s) from.
            value (T | Iterable[T]): Value or values to set at indices.

        Returns:
            Nothing

        Raises:
            IndexError: on invalid index.
            ValueError: index is a slice but value is not an iterable.
        """
        if isinstance(index, slice):
            if not isinstance(value, Iterable):
                raise ValueError("slice set item value must be iterable")
            self._setitem_slice(index, value)
            return
        self._node_getitem(index).value = cast("T", value)

    def _setitem_slice(
        self,
        slice_: slice[int | None, int | None, int | None],
        iterable: Iterable[T],
    ) -> None:
        """Overwrite multiple elements at once."""
        for index, item in zip(
            range(*slice_.indices(len(self))),
            iterable,
            strict=True,
        ):
            self[index] = item

    def insert(self, index: int, value: T) -> None:
        """Insert value before index.

        Find the node before given index and insert new node with given
        value right after the found node. If indexed node would fall
        before the head node or after the tail node, defaults to head or
        tail node.

        Args:
            index (int): Index to insert value before.
            value (T): Value to insert.

        Returns:
            Nothing.
        """

        if self.head is None:
            self.head = self.tail = Node(value)
            return
        if self.head == self.tail:
            index = min(0, max(-1, index))

        if index not in (0, -1):
            try:
                prior = self._node_getitem(index)
            except IndexError:
                # before an out of bounds is a head/tail update
                index = min(0, max(-1, -index))

        # head update
        if index == 0:
            old_head = self.head
            self.head = Node(value, old_head)
            old_head.prior = self.head
            return
        # tail update
        if index == -1:
            old_tail = self.tail
            assert old_tail is not None
            self.tail = Node(value, prior=old_tail)
            old_tail.next = self.tail
            return

        after = prior.next
        new = Node(value, after, prior)
        if prior is not None:
            prior.next = new
        if after is not None:
            after.prior = new

    def append(self, value: T) -> None:
        """Append value to the right side of the deque."""
        self.insert(-1, value)

    def appendleft(self, value: T) -> None:
        """Append value to the left side of the deque."""
        self.insert(0, value)

    addBack = append  # noqa: N815
    addFront = appendleft  # noqa: N815

    def extend(self, iterable: Iterable[T]) -> None:
        """Extend deque by appending elements from the iterable."""
        for item in iterable:
            self.append(item)

    def __iadd__(self, rhs: object | Iterable[T]) -> Self:
        """Self += rhs."""
        if not isinstance(rhs, Iterable):
            return NotImplemented
        self.extend(rhs)
        return self

    def __repr__(self) -> str:
        """Return representation of self."""
        items = ", ".join(map(repr, self))
        return f"{self.__class__.__name__}(({items}))"

    def pop(self, index: int = -1) -> T:
        """Remove and return item at index (default last).

        Args:
            index (int): Index value to pop index from.

        Returns:
            T object removed from given index.

        Raises:
            IndexError: if deque is empty or index is out of range.
        """
        node = self._node_getitem(index)
        prior = node.prior
        next_ = node.next

        if node is self.head:
            self.head = next_
        else:
            assert prior is not None
            prior.next = next_

        if node is self.tail:
            self.tail = prior
        else:
            assert next_ is not None
            next_.prior = prior

        # help gc
        node.next = None
        node.prior = None

        return node.value

    @overload
    def __delitem__(self, index: int, /) -> None: ...
    @overload
    def __delitem__(
        self,
        index: slice[int | None, int | None, int | None],
        /,
    ) -> None: ...

    def __delitem__(
        self,
        index: int | slice[int | None, int | None, int | None],
        /,
    ) -> None:
        """Delete item at given index.

        Args:
            index (int | slice[int | None, int | None, int | None]):
            Integer index or slice indices of value(s) to delete.

        Raises: IndexError on invalid index.
        """
        if isinstance(index, slice):
            self._delitem_slice(index)
            return
        self.pop(index)

    def _delitem_slice(
        self,
        slice_: slice[int | None, int | None, int | None],
    ) -> None:
        """Delete multiple elements."""
        # important to remove in descending order, or mid-update we will
        # screw up future deletions.
        slice_indices = sorted(range(*slice_.indices(len(self))), reverse=True)

        for index in slice_indices:
            del self[index]

    def clear(self) -> None:
        """Remove all items from deque."""
        # could just set head and tail to None but would leave a lot of
        # cyclical references that might not make gc happy.
        del self[:]

    def popleft(self) -> T:
        """Remove and return item from the front of the deque.

        Returns:
            Value removed from the front of the deque.

        Raises:
            IndexError: if deque is empty.
        """
        return self.pop(0)

    removeBack = pop  # noqa: N815
    removeFront = popleft  # noqa: N815

    def index(self, value: T, start: int = 0, stop: int | None = None) -> int:
        """Return first index of value.

        Args:
            value (T): Value to search for.
            start (int): Start index to start searching from.
            end (int | None): Index to stop searching at. If None,
            indicates search until end.

        Returns:
            Index an object equivalent to value was found at within
            given start and end indices.

        Raises:
            ValueError: if object equivalent to value is not present.
        """
        for index, item in enumerate(self):
            if index < start:
                continue
            if index == stop:
                break
            if item == value:
                return index
        raise ValueError("value not present")

    def __contains__(self, key: T) -> bool:
        """Return bool(key in self)."""
        try:
            self.index(key)
            return True
        except ValueError:
            return False

    search = __contains__

    # MutableSequence typing compliant version
    ##    def remove(self, value: T) -> None:
    ##        """Remove first occurrence of value.
    ##
    ##        Raises ValueError if the value is not present."""
    ##        # could be faster if we reimplement index and pop here because
    ##        # we could save the node instead of remembering offset steps and
    ##        # then re-retrieving it
    ##        self.pop(self.index(value))

    def remove(self, value: T) -> bool:
        """Return True if found and removed first occurrence of value."""
        try:
            index = self.index(value)
        except ValueError:
            return False
        self.pop(index)
        return True

##    def reverse(self) -> None:
##        """Reverse *IN PLACE*."""
##        if self.head is None or self.tail is None:
##            return
##
##        current_head = self.head
##        current_tail = self.tail
##
##        self.head, self.tail = self.tail, self.head
##
##        # 1234567
##        # ^     ^
##        # 7234561
##        #  ^   ^
##        # 7634521
##        #   ^ ^
##        # 7654321
##
##        while current_head is not current_tail:
##            head_forward = current_head.next
##            tail_backward = current_tail.prior
##            assert head_forward is not None
##            assert tail_backward is not None
##
##            head_backward = current_head.prior
##            tail_forward = current_tail.next
##
##            even_length_middle_swap = current_head.next is current_tail
##
##            # Start of swap connections to outer
##            if head_backward is not None:
##                head_backward.next = current_tail
##            current_tail.prior = head_backward
##
##            if tail_forward is not None:
##                tail_forward.prior = current_head
##            current_head.next = tail_forward
##
##            # Start of swap connections to inner
##            if even_length_middle_swap:
##                current_tail.next = current_head
##                current_head.prior = current_tail
##                break
##
##            current_tail.next = head_forward
##            head_forward.prior = current_tail
##
##            current_head.prior = tail_backward
##            tail_backward.next = current_head
##
##            # Next layer
##            current_head = head_forward
##            current_tail = tail_backward

    # Turns out this can be made way simpler just swapping the node
    # values instead of moving the nodes themselves around.
    def reverse(self) -> None:
        """Reverse *IN PLACE*."""
        if self.head is None or self.tail is None:
            return

        # 1234567
        # ^     ^
        # 7234561
        #  ^   ^
        # 7634521
        #   ^ ^
        # 7654321

        current_head = self.head
        current_tail = self.tail

        while current_head is not current_tail:
            even_length_middle_swap = current_head.next is current_tail

            # way easier to just swap values than try to swap connections
            current_head.value, current_tail.value = current_tail.value, current_head.value

            if even_length_middle_swap:
                break

            head_forward = current_head.next
            tail_backward = current_tail.prior
            assert head_forward is not None
            assert tail_backward is not None

            # Next layer
            current_head = head_forward
            current_tail = tail_backward

    def count(self, value: T) -> int:
        """Return number of occurrences of value."""
        return sum(element == value for element in self)


def run() -> None:
    """Run program."""
    test = Student("Waffles the Cat", 9, 3.78)
    print(test)
    test.set_name("Timmy")
    print(test)
    assert test.get_name() == "Timmy"
    assert test.get_age() == 9
    assert test.get_gpa() == 3.78

    # string equivalent to name field
    assert test == "Timmy"

    for string in ("123456", "1234567"):
        char_deque = Deque(string)
        print(char_deque)
        char_deque.reverse()
        print(char_deque)

    students = Deque((test,))
    students.addFront(Student("Mr. front seat", 10, 4.0))
    students.addBack(Student("Garfield", 9, 3.28))
    students.addFront(Student("Temp front person", 0, 0))
    students.addBack(Student("Temp back person", 0, 0))
    print("\n".join(map(repr, students)))
    assert students.removeFront() == "Temp front person"
    assert students.removeBack() == "Temp back person"
    # mypy does not like our Student equivalent to string shenanigans.
    # Could type as Deque[Student | str] to avoid.
    assert not students.search("Temp front person")  # type: ignore[arg-type]
    assert students.search("Garfield")  # type: ignore[arg-type]


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()
