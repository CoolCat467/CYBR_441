"""Graph."""

# Programmed by CoolCat467

from __future__ import annotations

# Graph
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

__title__ = "graph"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from node import Node


class Graph:
    """Graph class.

    nodes: the list of nodes, these should be node objects
    """

    __slots__ = ("nodes",)

    def __init__(self, nodes: list[Node] | None = None) -> None:
        """Initialize with optional initial nodes."""
        self.nodes: list[Node] = []

        if nodes is not None:
            self.nodes = nodes

    def __repr__(self) -> str:
        """Return representation of self."""
        return f"{self.__class__.__name__}({self.nodes!r})"

    def add_node(self, node: Node) -> None:
        """Add a node to the graph."""
        self.nodes.append(node)

    def get_nodes(self) -> list[Node]:
        """Return the list of all nodes."""
        return self.nodes

    def get_node(self, node_id: int) -> Node:
        """Return node from node id."""
        if node_id < 0 or node_id >= len(self.nodes):
            raise ValueError("Invalid node id")
        return self.nodes[node_id]

    def add_edge(self, source_id: int, dest_id: int) -> None:
        """Add connection from source id to dest id node."""
        self.get_node(source_id).add_connection(self.get_node(dest_id))

    def bfs(self, start_id: int) -> list[int]:
        """Return the Breadth First Search path to terminal starting at given node."""
        trail: dict[int, int] = {}

        to_visit = [start_id]
        while to_visit:
            current = to_visit.pop(0)
            if self.get_node(current).get_terminal():
                break
            for connected_node in self.get_node(current).get_connections():
                connected_id = connected_node.get_id()

                if connected_id in trail:
                    continue
                to_visit.append(connected_id)

                trail[connected_id] = current

        path: list[int] = []

        while current != start_id:
            path.insert(0, current)
            current = trail[current]
        path.insert(0, start_id)

        return path

    def _dfs_internal(
        self,
        start_id: int,
        visited: frozenset[int],
    ) -> tuple[bool, list[int]]:
        """Return tuple of success bool, node path list.

        Internal recursive depth first search helper.
        """
        current_node = self.get_node(start_id)

        if current_node.get_terminal():
            return True, [start_id]

        for connected_node in current_node.get_connections():
            connected_id = connected_node.get_id()
            if connected_id in visited:
                continue

            success, path = self._dfs_internal(
                connected_id,
                visited | {connected_id},
            )

            if success:
                return True, [start_id, *path]

        return False, []

    def dfs(self, start_id: int) -> list[int]:
        """Return the Depth First Search path to terminal starting at given node."""
        success, path = self._dfs_internal(start_id, frozenset((start_id,)))
        assert success
        return path
