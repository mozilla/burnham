# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import annotations

import logging
from abc import ABCMeta, abstractmethod
from typing import Any, ClassVar, Dict, Type

from burnham import metrics, pings
from burnham.exceptions import BurnhamError, ExperimentError
from burnham.experiments import Experiment

logger = logging.getLogger(__name__)


class WarpDrive:
    """Space-travel technology."""

    def __call__(self, coordinates: str) -> str:
        """Warp to the given coordinates."""

        metrics.technology.space_travel["warp_drive"].add(1)
        logger.debug("Warp to %s using space-travel technology", coordinates)

        return coordinates


class SporeDrive(Experiment):
    """Experimental space-travel technology."""

    identifier: ClassVar[str] = "spore_drive"

    def __call__(self, coordinates: str) -> str:
        """Jump to the given coordinates."""

        metrics.technology.space_travel["spore_drive"].add(1)
        logger.debug(
            "Jump to %s using experimental space-travel technology", coordinates
        )

        if coordinates == "Starbase 46":
            # The error message will be set for the Glean status metric.
            # This will produce a Glean validation error as the message
            # exceeds the maximum length for Glean string metric types.
            raise ExperimentError(
                "INCOMPLETE NAVIGATION SEQUENCE "
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

        return coordinates


class Discovery:
    """Spaceship that uses space-travel technology."""

    warp_drive: WarpDrive
    spore_drive: SporeDrive
    position: str = "starbase"
    missions: Dict[str, Type[MissionBase]] = {}

    def __init__(self, *, warp_drive: WarpDrive, spore_drive: SporeDrive) -> None:
        """Spaceship that uses technology for space travel."""
        self.warp_drive = warp_drive
        self.spore_drive = spore_drive

    def warp(self, coordinates: str) -> None:
        """Warp to the given coordinates using the WarpDrive."""
        self.position = self.warp_drive(coordinates)

    def jump(self, coordinates: str) -> None:
        """Jump to the given coordinates using the SporeDrive.

        This requires the SporeDrive Experiment to be active.
        """
        self.position = self.spore_drive(coordinates)

    def complete_mission(self, identifier: str) -> Any:
        """Complete the mission with the given identifier."""
        try:
            logger.debug("Starting mission '%s'", identifier)
            metrics.mission.identifier.set(identifier)
            self.missions[identifier].complete(self)
        except BurnhamError as err:
            logger.debug("Error completing mission '%s': %s", identifier, err)
            # This will produce a Glean validation error for BurnhamError
            # messages that exceed the maximum length for Glean string metric types.
            metrics.mission.status.set(f"ERROR: {err}")
        else:
            logger.debug("Completed mission '%s'", identifier)
            metrics.mission.status.set("COMPLETED")
        finally:
            # Make sure we submit a discovery ping
            logger.debug("Submitting ping for mission '%s'", identifier)
            pings.discovery.submit()


class MissionBase(metaclass=ABCMeta):
    """Abstract base class which registers subclasses with the Discovery."""

    @classmethod
    def __init_subclass__(cls: Type[MissionBase], *, identifier: str, **kwargs):
        super().__init_subclass__()

        # Register missions with the Discovery
        Discovery.missions[identifier] = cls

    @classmethod
    @abstractmethod
    def complete(cls, space_ship: Discovery) -> None:
        """Subclasses define and run a series of tasks for the space ship."""


class MissionA(MissionBase, identifier="MISSION A: ONE WARP"):
    """Warp one time."""

    @classmethod
    def complete(cls, space_ship: Discovery) -> None:
        space_ship.warp("abcdefgh")


class MissionB(MissionBase, identifier="MISSION B: TWO WARPS"):
    """Warp two times."""

    @classmethod
    def complete(cls, space_ship: Discovery) -> None:
        space_ship.warp("26.2")
        space_ship.warp("abc")


class MissionC(MissionBase, identifier="MISSION C: ONE JUMP"):
    """Jump one time."""

    @classmethod
    def complete(cls, space_ship: Discovery) -> None:
        space_ship.jump("12345")


class MissionD(MissionBase, identifier="MISSION D: TWO JUMPS"):
    """Jump two times."""

    @classmethod
    def complete(cls, space_ship: Discovery) -> None:
        space_ship.jump("2016")
        space_ship.jump("Berlin")


class MissionE(MissionBase, identifier="MISSION E: ONE JUMP, ONE METRIC ERROR"):
    """Jump one time to Starbase 46."""

    @classmethod
    def complete(cls, space_ship: Discovery) -> None:
        # This will produce a Glean validation error.
        # Check out the SporeDrive class for more information.
        space_ship.jump("Starbase 46")


class MissionF(MissionBase, identifier="MISSION F: TWO WARPS, ONE JUMP"):
    """Warp two times and jump one time."""

    @classmethod
    def complete(cls, space_ship: Discovery) -> None:
        space_ship.warp("abc")
        space_ship.warp("de")
        space_ship.jump("12345")


class MissionG(MissionBase, identifier="MISSION G: FIVE WARPS, FOUR JUMPS"):
    """Warp five times and jump four times."""

    @classmethod
    def complete(cls, space_ship: Discovery) -> None:
        space_ship.jump("1234")
        space_ship.warp("abcd")
        space_ship.warp("ab")
        space_ship.jump("8000")
        space_ship.jump("20")
        space_ship.jump("200")
        space_ship.warp("home")
        space_ship.warp("4000")
        space_ship.warp("abc123")
