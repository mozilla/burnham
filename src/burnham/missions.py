# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import Dict, Type

from burnham import pings
from burnham.space_travel import Discovery


class MissionBase:
    """Base class that has a mapping from names to subclasses."""

    missions: Dict[str, Type[MissionBase]] = {}

    @classmethod
    def __init_subclass__(cls: Type[MissionBase], name: str, **kwargs):
        super().__init_subclass__()
        cls.missions[name] = cls

    @classmethod
    def start(cls, space_ship: Discovery) -> None:
        """Subclasses define objectives for the given space_ship."""


class OneWarp(MissionBase, name="one_warp"):
    """Warp one time.

    This also submits one Glean ping.
    """

    @classmethod
    def start(cls, space_ship: Discovery) -> None:
        space_ship.warp("abc")
        pings.discovery.submit()


class OneJump(MissionBase, name="one_jump"):
    """Jump one time.

    This also submits one Glean ping.
    """

    @classmethod
    def start(cls, space_ship: Discovery) -> None:
        space_ship.jump("12345")
        pings.discovery.submit()


class OneJumpToUnknownDestination(MissionBase, name="one_jump_to_unknown_destination"):
    """Jump one time to an unknown destination.

    This also submits one Glean ping containing a validation error.
    """

    @classmethod
    def start(cls, space_ship: Discovery) -> None:
        space_ship.jump(
            "abcdabcdabcdabcdabcdabcd"
            "123412341234123412341234"
            "abcdabcdabcdabcdabcdabcd"
            "123412341234123412341234"
            "123412341234123412341234"
            "123412341234123412341234"
            "123412341234123412341234"
            "abcdabcdabcdabcdabcdabcd"
            "abcdabcdabcdabcdabcdabcd"
            "abcdabcdabcdabcdabcdabcd"
            "abcdabcdabcdabcdabcdabcd"
        )
        pings.discovery.submit()


class TwoWarpsAndOneJump(MissionBase, name="two_warps_and_one_jump"):
    """Warp two times and jump one time.

    This also submits two Glean pings.
    """

    @classmethod
    def start(cls, space_ship: Discovery) -> None:
        space_ship.warp("abc")
        pings.discovery.submit()
        space_ship.warp("de")
        space_ship.jump("12345")
        pings.discovery.submit()


class FiveWarpsAndFourJumps(MissionBase, name="five_warps_and_four_jumps"):
    """Warp five times and jump four times.

    This also submits four Glean pings.
    """

    @classmethod
    def start(cls, space_ship: Discovery) -> None:
        space_ship.jump("1234")
        space_ship.warp("abcd")
        space_ship.warp("ab")
        pings.discovery.submit()
        space_ship.jump("starbase")
        pings.discovery.submit()
        space_ship.jump("20")
        space_ship.jump("200")
        space_ship.warp("starbase")
        space_ship.warp("4000")
        pings.discovery.submit()
        space_ship.warp("abc123")
        pings.discovery.submit()
