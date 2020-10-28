# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import annotations

from typing import ClassVar

import pytest

from burnham.exceptions import ExperimentError
from burnham.experiments import Experiment


class Robot(Experiment):
    """Experimental AI technology."""

    identifier: ClassVar[str] = "robot"

    def __call__(self) -> str:
        return f"{self.identifier}:{self.branch} 🤖"


def test_active_robot():
    """Test that calling an active experiment does not raise an exception."""

    robot = Robot(active=True)

    assert robot() == "robot:default 🤖"


def test_inactive_robot():
    """Test that calling an inactive experiment raises an exception."""

    robot = Robot(branch="hello-world")

    with pytest.raises(ExperimentError) as excinfo:
        robot()

    assert "Experiment 'robot:hello-world' is inactive." in str(excinfo.value)


def test_activate_robot():
    """Test activating an experiment."""

    robot = Robot(active=False, branch="hello-world")
    robot.active = True

    assert robot() == "robot:hello-world 🤖"


def test_deactivate_robot():
    """Test that calling an inactive experiment raises an exception."""

    robot = Robot(active=True)
    robot.active = False

    with pytest.raises(ExperimentError) as excinfo:
        robot()

    assert "Experiment 'robot:default' is inactive." in str(excinfo.value)
