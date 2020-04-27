# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import annotations

import logging
from typing import Any, ClassVar, Dict, List

from typing_extensions import Protocol

from burnham import metrics, pings
from burnham.exceptions import BurnhamError
from burnham.space_travel import Discovery

logger = logging.getLogger(__name__)


class Mission(Protocol):
    """Protocol for space_travel missions."""

    identifier: ClassVar[str]

    def complete(self, space_ship: Discovery) -> None:
        """Subclasses define and run a series of tasks for the space ship."""


def complete_mission(*, space_ship: Discovery, mission: Mission) -> Any:
    """Complete the mission with the given identifier."""
    try:
        logger.debug("Starting mission '%s'", mission.identifier)
        metrics.mission.identifier.set(mission.identifier)
        mission.complete(space_ship=space_ship)
    except BurnhamError as err:
        logger.debug("Error completing mission '%s': %s", mission.identifier, err)
        # This will produce a Glean validation error for BurnhamError
        # messages that exceed the maximum length for Glean string metric types.
        metrics.mission.status.set(f"ERROR: {err}")
    else:
        logger.debug("Completed mission '%s'", mission.identifier)
        metrics.mission.status.set("COMPLETED")
    finally:
        # Make sure we submit a discovery ping
        logger.debug("Submitting ping for mission '%s'", mission.identifier)
        pings.discovery.submit()


class MissionA:
    """Warp one time."""

    identifier: ClassVar[str] = "MISSION A: ONE WARP"

    def complete(self, space_ship: Discovery) -> None:
        space_ship.warp("abcdefgh")


class MissionB:
    """Warp two times."""

    identifier: ClassVar[str] = "MISSION B: TWO WARPS"

    def complete(self, space_ship: Discovery) -> None:
        space_ship.warp("26.2")
        space_ship.warp("abc")


class MissionC:
    """Jump one time."""

    identifier: ClassVar[str] = "MISSION C: ONE JUMP"

    def complete(self, space_ship: Discovery) -> None:
        space_ship.jump("12345")


class MissionD:
    """Jump two times."""

    identifier: ClassVar[str] = "MISSION D: TWO JUMPS"

    def complete(self, space_ship: Discovery) -> None:
        space_ship.jump("2016")
        space_ship.jump("Berlin")


class MissionE:
    """Jump one time to Starbase 46."""

    identifier: ClassVar[str] = "MISSION E: ONE JUMP, ONE METRIC ERROR"

    def complete(self, space_ship: Discovery) -> None:
        # This will produce a Glean validation error.
        # Check out the SporeDrive class for more information.
        space_ship.jump("Starbase 46")


class MissionF:
    """Warp two times and jump one time."""

    identifier: ClassVar[str] = "MISSION F: TWO WARPS, ONE JUMP"

    def complete(self, space_ship: Discovery) -> None:
        space_ship.warp("abc")
        space_ship.warp("de")
        space_ship.jump("12345")


class MissionG:
    """Warp five times and jump four times."""

    identifier: ClassVar[str] = "MISSION G: FIVE WARPS, FOUR JUMPS"

    def complete(self, space_ship: Discovery) -> None:
        space_ship.jump("1234")
        space_ship.warp("abcd")
        space_ship.warp("ab")
        space_ship.jump("8000")
        space_ship.jump("20")
        space_ship.jump("200")
        space_ship.warp("home")
        space_ship.warp("4000")
        space_ship.warp("abc123")


missions: List[Mission] = [
    MissionA(),
    MissionB(),
    MissionC(),
    MissionD(),
    MissionE(),
    MissionF(),
    MissionG(),
]

missions_by_identifier: Dict[str, Mission] = {
    mission.identifier: mission for mission in missions
}
