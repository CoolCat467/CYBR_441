"""Node."""

# Programmed by CoolCat467

from __future__ import annotations

# Node
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

__title__ = "node"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from os import PathLike
    from typing import Self


class Node:
    """Node.

    Attributes:
        image: an image file (.png works) that shows the state
        id: the id for the state
        connections:
            a list of the other states that can be reached from this
            state
        terminal: is this state a solution

    """

    __slots__ = ("connections", "id_", "image", "terminal")

    def __init__(
        self,
        image: str | PathLike[str] | None = None,
        node_id: int = -1,
        terminal: bool = False,
    ) -> None:
        """Initialize node."""
        self.image = image
        self.id_ = node_id
        self.connections: list[Self] = []
        self.terminal = terminal

    def __repr__(self) -> str:
        """Return representation of self."""
        return f"{self.__class__.__name__}({self.get_image()!r}, {self.get_id()!r}, {self.get_terminal()!r})"

    def get_image(self) -> str | PathLike[str] | None:
        """Return optional state image path."""
        return self.image

    def get_id(self) -> int:
        """Return state id number."""
        return self.id_

    def get_connections(self) -> list[Self]:
        """Return connected states."""
        return self.connections

    def get_terminal(self) -> bool:
        """Return if this state is terminal."""
        return self.terminal

    def set_image(self, image: str | PathLike[str] | None) -> None:
        """Set this state's image file path."""
        self.image = image

    def set_id(self, node_id: int) -> None:
        """Set this state's id."""
        self.id_ = node_id

    def add_connection(self, other_node: Self) -> None:
        """Add connection to another node if the connection doesn't exist already."""
        if other_node in self.connections:
            return
        self.connections.append(other_node)
