# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import annotations

import logging
from typing import ClassVar

from burnham import metrics
from burnham.exceptions import ExperimentError
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
