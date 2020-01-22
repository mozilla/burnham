# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import ClassVar

from burnham.experiments import Experiment


class WarpDrive:
    """Space-travel technology."""

    def __call__(self, coordinates: str) -> str:
        return coordinates


class SporeDrive(Experiment):
    """Experimental space-travel technology."""

    identifier: ClassVar[str] = "spore_drive"

    def __call__(self, coordinates: str) -> str:
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

        This requires the SporeDrive Experiment to be added and active.
        """
        self.position = self.spore_drive(coordinates)
