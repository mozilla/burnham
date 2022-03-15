# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import annotations

import logging
import uuid
from typing import Any, Callable

import pytest
from click.testing import CliRunner, Result

from burnham import metrics
from burnham.cli import burnham


@pytest.fixture(name="run_cli")
def fixture_run_cli() -> Callable:
    """Return a function that invokes a click CLI runner."""

    # Disable the Glean SDK ping upload for all CLI tests
    runner = CliRunner(env={"BURNHAM_TELEMETRY": "0"})

    def run(*cli_options: str) -> Result:
        """Run the CLI with the given options and return the result."""
        return runner.invoke(burnham, cli_options)

    return run


def test_help(run_cli: Callable) -> None:
    """Test for the help option."""

    result = run_cli("--help")

    assert result.exit_code == 0
    assert "Usage: burnham" in result.output


@pytest.mark.parametrize("option", ["-V", "--version"])
def test_version(run_cli: Callable, option: str) -> None:
    """Test for the version options."""

    result = run_cli(option)

    assert result.exit_code == 0
    assert "burnham, version" in result.output


def test_cli(
    monkeypatch_space_ship_ready,
    monkeypatch_discovery,
    monkeypatch_starbase46,
    run_cli: Callable,
    caplog: Any,
) -> None:
    """Test for the CLI app."""
    caplog.set_level(logging.DEBUG)

    missions = [
        "MISSION A: ONE WARP",
        "MISSION E: ONE JUMP, ONE METRIC ERROR",
        "MISSION G: FIVE WARPS, FOUR JUMPS",
    ]

    result = run_cli(
        f"--test-run={uuid.uuid4()}",
        "--test-name=test_cli",
        "--airflow-task-id=client1",
        "--platform=localhost:0",
        "--spore-drive=tardigrade-dna",
        *missions,
    )

    assert result.exit_code == 0

    for mission in missions:
        assert f"Starting mission '{mission}'" in caplog.text
        assert f"Submitting ping for mission '{mission}'" in caplog.text

    assert monkeypatch_space_ship_ready.counter == 1
    assert monkeypatch_discovery.counter == 3
    assert monkeypatch_starbase46.counter == 1


def test_cli_verbosity(
    monkeypatch_space_ship_ready,
    monkeypatch_discovery,
    run_cli: Callable,
) -> None:
    """Test for verbosity in the CLI app."""

    missions = [
        "MISSION A: ONE WARP",
    ]

    result = run_cli(
        f"--test-run={uuid.uuid4()}",
        "--test-name=test_cli",
        "--airflow-task-id=client2",
        "--platform=localhost:0",
        "--verbose",
        *missions,
    )

    assert result.exit_code == 0

    assert monkeypatch_space_ship_ready.counter == 1
    assert monkeypatch_discovery.counter == 1


def test_cli_unknown_mission_identifier(
    monkeypatch_space_ship_ready, monkeypatch_discovery, run_cli: Callable
) -> None:
    """Test for error handling in the custom MissionParamType."""

    missions = [
        "MISSION A: ONE WARP",
        "MISSION Z: TEST",
        "MISSION B: TWO WARPS",
    ]

    result = run_cli(
        f"--test-run={uuid.uuid4()}",
        "--test-name=test_cli",
        "--airflow-task-id=client3",
        "--platform=localhost:0",
        "--spore-drive=tardigrade-dna",
        *missions,
    )

    assert 'Unknown mission identifier "MISSION Z: TEST"' in result.output
    assert result.exit_code == 2

    assert monkeypatch_space_ship_ready.counter == 0
    assert monkeypatch_discovery.counter == 0


def test_cli_restore_test_run_and_test_name(
    monkeypatch_space_ship_ready,
    monkeypatch_discovery,
    monkeypatch_set_upload_enabled,
    run_cli: Callable,
) -> None:
    """Test that the CLI restores the values for test.run and test.name after
    completing MISSION I.
    """

    missions = [
        "MISSION G: FIVE WARPS, FOUR JUMPS",
        "MISSION H: DISABLE GLEAN UPLOAD",
        "MISSION D: TWO JUMPS",
        "MISSION I: ENABLE GLEAN UPLOAD",
    ]

    result = run_cli(
        f"--test-run={uuid.uuid4()}",
        "--test-name=test_cli",
        "--airflow-task-id=client4",
        "--platform=localhost:0",
        "--spore-drive=tardigrade-dna",
        *missions,
    )

    assert result.exit_code == 0

    assert monkeypatch_set_upload_enabled.values == [False, True]
    assert monkeypatch_space_ship_ready.counter == 1
    assert monkeypatch_discovery.counter == 4


def test_cli_metrics(
    monkeypatch_space_ship_ready,
    monkeypatch_discovery,
    monkeypatch_starbase46,
    run_cli: Callable,
) -> None:
    """Test that the CLI app sets Glean metrics as expected."""

    missions = [
        "MISSION A: ONE WARP",
        "MISSION G: FIVE WARPS, FOUR JUMPS",
    ]

    test_run = uuid.uuid4()
    test_name = "test_cli"
    airflow_task_id = "client5"

    result = run_cli(
        f"--test-run={test_run}",
        f"--test-name={test_name}",
        f"--airflow-task-id={airflow_task_id}",
        "--platform=localhost:0",
        "--spore-drive=tardigrade-dna",
        *missions,
    )

    assert result.exit_code == 0

    assert metrics.test.run.test_get_value() == test_run
    assert metrics.test.name.test_get_value() == test_name
    assert metrics.test.airflow_task_id.test_get_value() == airflow_task_id

    assert monkeypatch_space_ship_ready.counter == 1
    assert monkeypatch_discovery.counter == 2
    assert monkeypatch_starbase46.counter == 0
