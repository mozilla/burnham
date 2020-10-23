# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import annotations

import pytest
from glean import Glean, testing


class SpyPing:
    """Spy class for Glean pings that counts the number of times submit is called."""

    def __init__(self) -> None:
        self.counter = 0

    def submit(self) -> None:
        self.counter += 1


@pytest.fixture(name="initialize_glean", scope="session", autouse=True)
def fixture_initialize_glean(tmp_path_factory):
    """Initialize the Glean SDK for the test session."""

    Glean.initialize(
        application_id="burnham_testing",
        application_version="0.1.0",
        upload_enabled=False,
        data_dir=tmp_path_factory.mktemp("glean"),
    )


@pytest.fixture(name="reset_glean", scope="function", autouse=True)
def fixture_reset_glean():
    """Reset the Glean SDK before every test."""

    testing.reset_glean(application_id="burnham_testing", application_version="0.1.0")


@pytest.fixture(name="monkeypatch_discovery")
def fixture_monkeypatch_discovery(monkeypatch) -> SpyPing:
    """Monkeypatch the discovery ping."""
    discovery = SpyPing()
    monkeypatch.setattr("burnham.missions.pings.discovery", discovery)
    return discovery


@pytest.fixture(name="monkeypatch_starbase46")
def fixture_monkeypatch_starbase46(monkeypatch) -> SpyPing:
    """Monkeypatch the starbase46 ping."""
    starbase46 = SpyPing()
    monkeypatch.setattr("burnham.missions.pings.starbase46", starbase46)
    return starbase46


@pytest.fixture(name="monkeypatch_space_ship_ready")
def fixture_monkeypatch_space_ship_ready(monkeypatch) -> SpyPing:
    """Monkeypatch the space_ship_ready ping."""
    space_ship_ready = SpyPing()
    monkeypatch.setattr("burnham.cli.pings.space_ship_ready", space_ship_ready)
    return space_ship_ready
