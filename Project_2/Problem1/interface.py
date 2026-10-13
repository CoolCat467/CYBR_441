"""Interface."""

# Programmed by CoolCat467

from __future__ import annotations

# Interface
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

__title__ = "interface"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"

import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from typing import TYPE_CHECKING, Final

from world import World

if TYPE_CHECKING:
    from graph import Graph
    from state import Action

MAX_GENERATED_TILES: Final = 5


class GraphInterface:
    """Graph Interface tkinter application."""

    def __init__(self) -> None:
        """Initialize graph interface."""
        self.__world = World(2)

        self.__path: list[tuple[int, Action | None]] = []
        self.__current_step = 0
        self.__photo: tk.PhotoImage | None = None

        self.__window = tk.Tk()
        self.__window.title("Graph Search")

        # Start node input
        tk.Label(
            self.__window,
            text=f"Tile Count: (2-{MAX_GENERATED_TILES})",
        ).grid(row=0, column=0, padx=30, pady=5)

        self.__tiles_entry = tk.Entry(self.__window)
        self.__tiles_entry.insert(0, "2")
        self.__tiles_entry.grid(row=0, column=1, padx=30, pady=5)

        # Start node input
        tk.Label(
            self.__window,
            text=f"Start Node ID: (0-{len(self.__graph.get_nodes()) - 1})",
        ).grid(row=1, column=0, padx=30, pady=5)

        self.__start_entry = tk.Entry(self.__window)
        self.__start_entry.insert(0, "0")
        self.__start_entry.grid(row=1, column=1, padx=30, pady=5)

        # Search buttons
        tk.Button(
            self.__window,
            text="Solve BFS",
            command=self.solve_bfs,
        ).grid(row=2, column=0, padx=30, pady=20)

        tk.Button(
            self.__window,
            text="Solve DFS",
            command=self.solve_dfs,
        ).grid(row=2, column=1, padx=30, pady=20)

        # Image display
        self.__image_label = tk.Label(self.__window)
        self.__image_label.grid(row=3, column=0, columnspan=2, pady=40)

        # Information label
        self.__info_label = tk.Label(self.__window, text="No solution loaded.")

        self.__info_label.grid(row=4, column=0, columnspan=2)

        # Navigation buttons
        tk.Button(
            self.__window,
            text="Previous",
            command=self.previous_state,
        ).grid(row=5, column=0, pady=10)

        tk.Button(self.__window, text="Next", command=self.next_state).grid(
            row=5,
            column=1,
            pady=10,
        )

    def reload_world(self) -> bool:
        """Return if loaded new world successfully."""
        try:
            tile_count = int(self.__tiles_entry.get())
            if tile_count < 2 or tile_count > MAX_GENERATED_TILES:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter a valid tile count.",
            )
            return False
        # Regenerate world
        if self.__world.get_tile_count() != tile_count:
            self.__world = World(tile_count)
        return True

    @property
    def __graph(self) -> Graph:
        """Return current world graph."""
        return self.__world.get_graph()

    def solve_bfs(self) -> None:
        """Solve with breadth first search with current parameters."""
        if not self.reload_world():
            return

        try:
            start_id = int(self.__start_entry.get())

            ######
            # NOTE: This is where it is calling your function
            ######
            self.__path = self.__graph.bfs(start_id)
            self.__current_step = 0
            print(f"Path for BFS: {self.__path}")
            if not self.__path:
                messagebox.showinfo("No Solution", "No goal node was found.")
                return

            self.show_current_state()

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter a valid node ID.",
            )

    def solve_dfs(self) -> None:
        """Solve with depth first search with current parameters."""
        if not self.reload_world():
            return

        try:
            start_id = int(self.__start_entry.get())

            ######
            # NOTE: This is where it is going to call your function
            ######
            self.__path = self.__graph.dfs(start_id)
            self.__current_step = 0
            print(f"Path for DFS: {self.__path}")
            if not self.__path:
                messagebox.showinfo("No Solution", "No goal node was found.")
                return

            self.show_current_state()

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter a valid node ID.",
            )

    def show_current_state(self) -> None:
        """Display the current state."""
        if not self.__path:
            return

        node_id, action = self.__path[self.__current_step]

        node = self.__graph.get_node(node_id)

        node_image = node.get_image()
        image_path: Path | None = None
        if node_image is not None:
            image_path = Path(node_image).absolute()

        self.__photo = tk.PhotoImage(file=str(image_path))

        self.__image_label.config(image=self.__photo)

        action_text = "<initial state>"
        goal_text = ""

        if action is not None:
            action_text = action.name

        if node.get_terminal():
            goal_text = " (GOAL)"

        self.__info_label.config(
            text="\n".join(
                (
                    f"Step {self.__current_step + 1}/{len(self.__path)}",
                    f"    Node ID: {node_id}",
                    f"    Previous Action: {action_text}",
                    f"{goal_text}",
                ),
            ),
        )

    def next_state(self) -> None:
        """Display the next state."""
        if not self.__path:
            return

        if self.__current_step < len(self.__path) - 1:
            self.__current_step += 1
            self.show_current_state()

    def previous_state(self) -> None:
        """Display the prior state."""
        if not self.__path:
            return

        if self.__current_step > 0:
            self.__current_step -= 1
            self.show_current_state()

    def run(self) -> None:
        """Run tkinter main loop."""
        self.__window.mainloop()


def run() -> None:
    """Run application."""
    gui = GraphInterface()
    gui.run()


if __name__ == "__main__":
    run()
