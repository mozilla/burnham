# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


def pytest_addoption(parser):
    """Hook implementation that adds a "--results-table" CLI option."""

    burnham_group = parser.getgroup("burnham")
    burnham_group.addoption(
        "--results-table",
        action="store",
        dest="results_table",
        help="BigQuery table for storing results",
        metavar="TABLE",
        type=str,
        required=False,
    )


class StoreResults:
    """Plugin for storing test results in BigQuery."""

    def __init__(self, config) -> None:
        self.config = config


def pytest_configure(config) -> None:
    """Hook implementation that registers the plugin."""

    results_table = config.getoption("results_table")

    if results_table is None:
        return

    config.pluginmanager.register(StoreResults(config), "bigquery_store_results")


def pytest_unconfigure(config) -> None:
    """Hook implementation that unregisters the plugin."""

    plugin = config.pluginmanager.get_plugin("bigquery_store_results")

    if plugin is None:
        return

    config.pluginmanager.unregister(plugin)
