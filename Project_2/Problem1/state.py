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
    from typing import Self


class State(NamedTuple):
    """Vacuum world state tuple."""

    location: int
    dust: tuple[bool, ...]

    @classmethod
    def initial_state(cls, tile_count: int) -> Self:
        """Return an initial state for a world with a given number of tiles."""
        return cls(0, tuple(True for _ in range(tile_count)))

    def __str__(self) -> str:
        """Return a string representation of the world."""
        dust = "".join("▓" if dust else "▒" for dust in self.dust)
        indicator = " " * self.location + "^"
        return f"{dust}\n{indicator}"

    @classmethod
    def new_state(cls, location: int, dust: tuple[bool, ...]) -> Self:
        """Return a new state instance."""
        return cls(location, dust)

    def action_clean(self) -> Self:
        """Return a new world state after performing the clean action."""
        if not self.dust[self.location]:
            return self
        return self.new_state(
            self.location,
            # tile dust is the same except for the tile the robot is
            # currently on, which is set to false if not already.
            tuple(
                dust if idx != self.location else False
                for idx, dust in enumerate(self.dust)
            ),
        )

    def action_left(self) -> Self:
        """Return a new world state after performing the move left action.

        Trying to move beyond the edge of the map does nothing.
        """
        new_location = max(0, self.location - 1)
        if new_location == self.location:
            return self
        return self.new_state(new_location, self.dust)

    def action_right(self) -> Self:
        """Return a new world state after performing the move right action.

        Trying to move beyond the edge of the map does nothing.
        """
        new_location = min(self.location + 1, len(self.dust) - 1)
        if new_location == self.location:
            return self
        return self.new_state(new_location, self.dust)

    def actions(self) -> tuple[Self, Self, Self]:
        """Return the results of all possible actions able to be performed at this state."""
        return (
            self.action_left(),
            self.action_clean(),
            self.action_right(),
        )

    def redundant_actions(
        self,
    ) -> tuple[tuple[bool, Self], tuple[bool, Self], tuple[bool, Self]]:
        """Return tuple of bool and new state tuples where True is a redundant action."""
        return tuple((state is self, state) for state in self.actions())

    def terminal(self) -> bool:
        """Return if there is not any dust remaining in the world."""
        return not any(self.dust)

    def repr_id(self) -> str:
        """Return a representation of this state as an identifier string.

        Follows {location}_{tile dust states}.
        """
        dust_data = "".join(str(int(dust)) for dust in self.dust)
        return f"{self.location}_{dust_data}"
