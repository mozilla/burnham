# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import annotations

import logging

import pytest

from burnham import metrics
from burnham.exceptions import ExperimentError
from burnham.missions import complete_mission, missions_by_identifier
from burnham.space_travel import Discovery, SporeDrive, WarpDrive


@pytest.fixture(name="space_ship")
def fixture_space_ship():
    """Return a Discovery instance with spore_drive active."""
    return Discovery(
        warp_drive=WarpDrive(),
        spore_drive=SporeDrive(branch="tardigrade", active=True),
    )


def test_mission_a(space_ship: Discovery) -> None:
    """Test for Mission A."""
    mission = missions_by_identifier["MISSION A: ONE WARP"]
    mission.complete(space_ship=space_ship)
    assert metrics.technology.space_travel["warp_drive"].test_get_value() == 1


def test_mission_b(space_ship: Discovery) -> None:
    """Test for Mission B."""
    mission = missions_by_identifier["MISSION B: TWO WARPS"]
    mission.complete(space_ship=space_ship)
    assert metrics.technology.space_travel["warp_drive"].test_get_value() == 2


def test_mission_c(space_ship: Discovery) -> None:
    """Test for Mission C."""
    mission = missions_by_identifier["MISSION C: ONE JUMP"]
    mission.complete(space_ship=space_ship)
    assert metrics.technology.space_travel["spore_drive"].test_get_value() == 1


def test_mission_d(space_ship: Discovery) -> None:
    """Test for Mission D."""
    mission = missions_by_identifier["MISSION D: TWO JUMPS"]
    mission.complete(space_ship=space_ship)
    assert metrics.technology.space_travel["spore_drive"].test_get_value() == 2


def test_mission_e(space_ship: Discovery) -> None:
    """Test for Mission E."""
    mission = missions_by_identifier["MISSION E: ONE JUMP, ONE METRIC ERROR"]

    with pytest.raises(ExperimentError) as excinfo:
        mission.complete(space_ship=space_ship)

    assert metrics.technology.space_travel["spore_drive"].test_get_value() == 1
    assert "INCOMPLETE NAVIGATION SEQUENCE" in str(excinfo.value)


def test_mission_f(space_ship: Discovery) -> None:
    """Test for Mission F."""
    mission = missions_by_identifier["MISSION F: TWO WARPS, ONE JUMP"]

    mission.complete(space_ship=space_ship)

    values = {
        "warp_drive": metrics.technology.space_travel["warp_drive"].test_get_value(),
        "spore_drive": metrics.technology.space_travel["spore_drive"].test_get_value(),
    }

    assert values == {"warp_drive": 2, "spore_drive": 1}


def test_mission_g(space_ship: Discovery) -> None:
    """Test for Mission G."""
    mission = missions_by_identifier["MISSION G: FIVE WARPS, FOUR JUMPS"]

    mission.complete(space_ship=space_ship)

    values = {
        "warp_drive": metrics.technology.space_travel["warp_drive"].test_get_value(),
        "spore_drive": metrics.technology.space_travel["spore_drive"].test_get_value(),
    }

    assert values == {"warp_drive": 5, "spore_drive": 4}


def test_mission_h(monkeypatch_set_upload_enabled, space_ship: Discovery) -> None:
    """Test for Mission H."""
    mission = missions_by_identifier["MISSION H: DISABLE GLEAN UPLOAD"]

    mission.complete(space_ship=space_ship)
    assert monkeypatch_set_upload_enabled.values == [False]


def test_mission_i(monkeypatch_set_upload_enabled, space_ship: Discovery) -> None:
    """Test for Mission I."""
    mission = missions_by_identifier["MISSION I: ENABLE GLEAN UPLOAD"]

    mission.complete(space_ship=space_ship)
    assert monkeypatch_set_upload_enabled.values == [True]


def test_complete_mission_status_completed(
    caplog, monkeypatch_discovery, space_ship: Discovery
):
    """Test that complete_mission emits the expected logs for a completed mission."""
    caplog.set_level(logging.DEBUG)

    identifier = "MISSION G: FIVE WARPS, FOUR JUMPS"
    mission = missions_by_identifier[identifier]

    complete_mission(space_ship=space_ship, mission=mission)

    assert f"Starting mission '{identifier}'" in caplog.text
    assert f"Completed mission '{identifier}'" in caplog.text
    assert f"Error completing mission '{identifier}':" not in caplog.text
    assert f"Submitting ping for mission '{identifier}'" in caplog.text
    assert monkeypatch_discovery.counter == 1


def test_complete_mission_status_error(
    caplog,
    monkeypatch_discovery,
    space_ship: Discovery,
):
    """Test that complete_mission emits the expected logs for an error mission."""
    caplog.set_level(logging.DEBUG)

    identifier = "MISSION E: ONE JUMP, ONE METRIC ERROR"
    mission = missions_by_identifier[identifier]

    complete_mission(space_ship=space_ship, mission=mission)

    assert f"Starting mission '{identifier}'" in caplog.text
    assert f"Completed mission '{identifier}'" not in caplog.text
    assert f"Error completing mission '{identifier}':" in caplog.text
    assert f"Submitting ping for mission '{identifier}'" in caplog.text
    assert monkeypatch_discovery.counter == 1
