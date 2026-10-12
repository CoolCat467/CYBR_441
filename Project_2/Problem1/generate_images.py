#!/usr/bin/env python3

"""Generate Images and state documentation.

Usage:
python generate_images.py > README.md
"""

# Programmed by CoolCat467

from __future__ import annotations

# Generate Images
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

__title__ = "Generate Images"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"

from os import environ, makedirs
from pathlib import Path
from typing import TYPE_CHECKING

environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import pygame
import render_images
from interface import MAX_GENERATED_TILES
from world import generate_graph_and_states

if TYPE_CHECKING:
    from node import Node
    from state import State


def state_to_picture(state: State) -> render_images.RenderedPicture:
    """Return RenderedPicture from a given State."""
    # Render state as text
    lines = str(state).splitlines()

    width = max(map(len, lines))
    height = len(lines)

    picture = render_images.RenderedPicture(width, height)

    bg = render_images.color.rgb_to_integer(18, 18, 18)

    fg_map = {
        " ": render_images.color.rgb_to_integer(18, 18, 18),
        "^": render_images.color.rgb_to_integer(255, 0, 0),
        "▒": render_images.color.rgb_to_integer(255, 255, 255),
        "▓": render_images.color.rgb_to_integer(127, 127, 127),
    }
    unknown_symbol_color = render_images.color.rgb_to_integer(0, 0, 255)

    # Draw image data
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            fg = fg_map.get(char, unknown_symbol_color)
            picture.set(x, y, char, fg, bg, 0)
    return picture


def render_node(node: Node, state: State, image_height: int) -> None:
    """Render node-state pair and save resulting image."""
    print(f"* {node.get_id()}\n```\n{state}\n```")
    image_path = Path(node.get_image()).absolute()

    if not image_path.parent.exists():
        makedirs(image_path.parent)

    picture = state_to_picture(state)

    font_size = picture.get_fontsize(image_height, image_height)
    surface = picture.render(font_size)

    pygame.image.save(surface, str(image_path))


def run() -> None:
    """Run program."""
    image_height = 200

    print("""# Vacuum World

## How to run application
- Have python 3 installed ([download](https://www.python.org/))
-
```bash
python interface.py
```
- Enter tile count (default 2)
- Enter initial state (default 0)
- Press either BFS or DFS search button
- Press through states with next and back buttons

## States""")

    for tile_count in range(2, MAX_GENERATED_TILES + 1):
        print(f"""\n## {tile_count} Tiles:
<details>
<summary>All {tile_count}-tile states</summary>
""")
        # print(f"Rendering states for {tile_count} tiles...")

        graph, states = generate_graph_and_states(tile_count)
        nodes = graph.get_nodes()

        for node in nodes:
            render_node(node, states[node.get_id()], image_height)
        # print(f"Rendered {len(nodes)} images.")
        print("</details>")
    # print("Action complete")


if __name__ == "__main__":
    # print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    try:
        pygame.init()
        run()
    finally:
        pygame.quit()
