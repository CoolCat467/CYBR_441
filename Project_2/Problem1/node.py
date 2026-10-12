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

    from typing_extensions import Self


class Node:
    '''
    image: an image file (.png works) that shows the state
    id: the id for the state
    connections: a list of the other states that can be reached from this state
    what else do you want to add...?
    '''

    __slots__ = ("image", "id_", "terminal", "connections")

    def __init__(
        self,
        image: str | PathLike[str] | None = None,
        node_id: int = -1,
        terminal: bool = False,
    ) -> None:
        self.image = image
        self.id_ = node_id
        self.connections: list[Self] = []
        self.terminal = terminal

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.get_image()!r}, {self.get_id()!r})"
        
    def get_image(self) -> str | PathLike[str] | None:
        return self.image

    def get_id(self) -> int:
        return self.id_

    def get_connections(self) -> list[Self]:
        return self.connections

    def get_terminal(self) -> bool:
        return self.terminal
    
    def set_image(self, image: str | PathLike[str] | None) -> None:
        self.image = image

    def set_id(self, node_id: int) -> None:
        self.id_ = node_id

    def add_connection(self, other_node: Self, action: None = None) -> None:
        if other_node in self.connections:
            return
        self.connections.append(other_node)
