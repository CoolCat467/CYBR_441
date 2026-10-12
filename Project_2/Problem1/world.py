"""World."""

# Programmed by CoolCat467

from __future__ import annotations

# world
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

__title__ = "world"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from pathlib import Path

from graph import Graph
from node import Node
from state import State


def add_new_state(
    state: State,
    state_id_map: dict[str, int],
    graph: Graph,
    id_state_map: dict[int, State],
) -> tuple[int, bool]:
    """Return new state id and if this state exists already.

    Add new state to graph and other places.
    """
    state_repr_id = state.repr_id()

    found_prev_id = state_id_map.get(state_repr_id)
    if found_prev_id is not None:
        return found_prev_id, True

    state_id = len(state_id_map)
    state_id_map[state_repr_id] = state_id
    id_state_map[state_id] = state

    image = Path("images") / f"{state_repr_id}.png"
    node = Node(image, state_id, state.terminal())

    graph.add_node(node)
    return state_id, False


def generate_graph_and_states(
    tile_count: int,
) -> tuple[Graph, dict[int, State]]:
    """Return tuple of graph and state dictionary for world with given tile count."""
    graph = Graph()

    state_id_map: dict[str, int] = {}
    id_state_map: dict[int, State] = {}

    initial_state = State.initial_state(tile_count)
    initial_id, _visited = add_new_state(
        initial_state,
        state_id_map,
        graph,
        id_state_map,
    )

    state_queue: list[tuple[int, State]] = [(initial_id, initial_state)]

    while state_queue:
        state_id, state = state_queue.pop(0)
        # print(f'{(state_id, state) = }')

        for redundant, new_state in state.redundant_actions():
            # print(f'{(redundant, new_state) = }')
            if redundant:
                graph.add_edge(state_id, state_id)
                continue

            new_state_id, visited = add_new_state(
                new_state,
                state_id_map,
                graph,
                id_state_map,
            )
            graph.add_edge(state_id, new_state_id)

            if visited:
                continue
            state_queue.append((new_state_id, new_state))
    return graph, id_state_map


def generate_graph(tile_count: int) -> Graph:
    """Return graph for world with given tile count."""
    graph, _states = generate_graph_and_states(tile_count)
    return graph


class World:
    """World class.

    Has a graph and tile count.
    """

    __slots__ = ("graph", "tiles")

    def __init__(self, num: int) -> None:
        """Initialize world from tile count."""
        self.tiles = num
        self.graph: Graph

        # num is how many cells in here, create your nodes connect them
        # to each other and add them to the graph object.  This will run
        # in the "main" of "interface.py"
        self.set_graph(generate_graph(num))

    def get_tile_count(self) -> int:
        return self.tiles

    def get_graph(self) -> Graph:
        assert self.graph is not None
        return self.graph

    def set_graph(self, gr: Graph) -> None:
        assert isinstance(gr, Graph)
        self.graph = gr
