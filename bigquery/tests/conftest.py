# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
from dataclasses import dataclass
from typing import Any, List

import pytest
from google.cloud.bigquery import Client


def pytest_addoption(parser):
    """Define custom CLI options."""
    burnham_group = parser.getgroup("burnham")
    burnham_group.addoption(
        "--run",
        action="store",
        dest="run",
        help="JSON encoded test run information",
        metavar="TEST_RUN_INFORMATION",
        type=str,
        required=True,
    )
    burnham_group.addoption(
        "--project",
        action="store",
        dest="project",
        help="BigQuery project ID",
        metavar="PROJECT_ID",
        type=str,
        required=True,
    )


@dataclass(frozen=True)
class Scenario:
    """Class that holds information about a specific test scenario."""

    name: str
    query: str
    want: List[List[Any]]


@dataclass(frozen=True)
class Run:
    """Class test runs with an ID and list of test scenarios."""

    identifier: str
    tests: List[Scenario]


def pytest_configure(config):
    """Load test run information from custom CLI options."""

    if config.option.run is not None:
        run = json.loads(config.option.run)

        config.burnham_run = Run(
            identifier=run["identifier"],
            tests=[Scenario(**scenario) for scenario in run["tests"]],
        )


def pytest_generate_tests(metafunc):
    """Generate tests from test run information."""

    ids = []
    argvalues = []

    for scenario in metafunc.config.burnham_run.tests:
        ids.append(scenario.name)
        argvalues.append([scenario.query, scenario.want])

    metafunc.parametrize(["query", "want"], argvalues, ids=ids)


@pytest.fixture(name="bq_client", scope="session")
def fixture_bq_client(request) -> Client:
    """Return a BigQuery client."""
    return Client(project=request.config.option.project)
