"""State."""

# Programmed by CoolCat467

from __future__ import annotations

# state
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

__title__ = "state"
__author__ = "CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from typing_extensions import Self


class State(NamedTuple):
    location: int
    tiles: tuple[bool, ...]

    @classmethod
    def initial_state(cls, tile_count: int) -> Self:
        return cls(0, tuple(True for _ in range(tile_count)))

    def __str__(self) -> str:
        tiles = ''.join('▓' if dust else '▒' for dust in self.tiles)
        indicator = " " * self.location + "^"
        return f"{tiles}\n{indicator}"

    @classmethod
    def new_state(cls, location: int, tiles: tuple[bool, ...]) -> Self:
        return cls(location, tiles)

    def action_clean(self) -> Self:
        if not self.tiles[self.location]:
            return self
        return self.new_state(
            self.location,
            tuple(
                dust if idx != self.location else False
                for idx, dust in enumerate(self.tiles)
            )
        )

    def action_left(self) -> Self:
        new_location = max(0, self.location - 1)
        if new_location == self.location:
            return self
        return self.new_state(new_location, self.tiles)

    def action_right(self) -> Self:
        new_location = min(self.location + 1, len(self.tiles) - 1)
        if new_location == self.location:
            return self
        return self.new_state(new_location, self.tiles)

    def actions(self) -> tuple[Self, Self, Self]:
        return (
            self.action_left(),
            self.action_clean(),
            self.action_right(),
        )

    def redundant_actions(self) -> tuple[tuple[bool, Self], tuple[bool, Self], tuple[bool, Self]]:
        """Return tuple of bools where True redundant actions."""
        return tuple((state is self, state) for state in self.actions())

    def terminal(self) -> bool:
        return not any(self.tiles)

    def repr_id(self) -> str:
        dust_data = "".join(str(int(dust)) for dust in self.tiles)
        return f"{self.location}_{dust_data}"
