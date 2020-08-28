# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


import io
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List

from google.cloud import bigquery

REPORT_TEMPLATE = """
# burnham-bigquery report

## Test information

📋 Column               | Value
----------------------- | -------------
📡 test_run             | {test_run}
🚀 test_name            | `{test_name}`
🤖 test_outcome         | {test_outcome}
🕗️ test_duration_millis | {test_duration_millis}
📅 submission_timestamp | {submission_timestamp}
📝 test_log_url         | [airflow log]

[airflow log]: {test_log_url}
"""

TRACEBACK_TEMPLATE = """
## Test traceback

```text
{traceback}
```
"""


class Outcome(Enum):
    """Enum for the different pytest outcomes."""

    ERROR = "ERROR"
    FAILED = "FAILED"
    PASSED = "PASSED"
    SKIPPED = "SKIPPED"
    XFAILED = "XFAILED"
    XPASSED = "XPASSED"
    WARNINGS = "WARNINGS"
    DESELECTED = "DESELECTED"


@dataclass(frozen=True)
class TableRow:
    """Dataclass representing a row in the results table.

    See https://github.com/mozilla/bigquery-etl/blob/master/sql/burnham_derived/test_results_v1/schema.bq.json
    """

    # Time at which this test report was submitted
    submission_timestamp: str
    # ID of the test run
    test_run: str
    # Name of the test scenario
    test_name: str
    # Outcome of the test scenario
    test_outcome: str
    # Duration of the test scenario
    test_duration_millis: int
    # URL for viewing logs of this task instance in Airflow
    test_log_url: str
    # Markdown-formatted report for error or failed tests
    test_report: str


def new_row(config: Any, outcome: Outcome, report: Any) -> TableRow:
    """Create a new TableRow for the given pytest report."""

    row_values: Dict[str, Any] = {
        "submission_timestamp": datetime.now(timezone.utc).isoformat(),
        "test_run": config.option.run_id,
        "test_name": report.nodeid,
        "test_outcome": outcome.value,
        "test_duration_millis": int(round(report.duration * 1000)),
        "test_log_url": config.option.log_url,
    }

    test_report: str = REPORT_TEMPLATE.format(**row_values)

    if outcome is Outcome.ERROR or outcome is Outcome.FAILED:
        test_report += TRACEBACK_TEMPLATE.format(traceback=report.longreprtext)

    return TableRow(test_report=test_report, **row_values)


def write_rows(client: bigquery.Client, table: str, rows: List[TableRow]) -> None:
    """Write the test results to the specified BigQuery table."""

    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.job.WriteDisposition.WRITE_APPEND,
    )

    data_str = "\n".join(json.dumps(asdict(row), ensure_ascii=False) for row in rows)
    data_file = io.BytesIO(data_str.encode(encoding="utf-8"))

    load_job = client.load_table_from_file(
        data_file, destination=table, job_config=job_config,
    )

    # Wait for load job to complete; raises an exception if the job failed.
    load_job.result()


class StoreResults:
    """Plugin for storing test results in BigQuery."""

    def __init__(self, config: Any) -> None:
        self.config = config
        self.table_rows: List[TableRow] = []

    def append_failed(self, report: Any) -> None:
        """Append a new TableRow for the failed report."""

        if report.when == "call":
            if hasattr(report, "wasxfail"):
                outcome = Outcome.XPASSED
            else:
                outcome = Outcome.FAILED
        else:
            outcome = Outcome.ERROR

        self.table_rows.append(new_row(self.config, outcome, report))

    def append_passed(self, report: Any) -> None:
        """Append a new TableRow for the passed report."""

        if report.when == "call":
            if hasattr(report, "wasxfail"):
                outcome = Outcome.XPASSED
            else:
                outcome = Outcome.PASSED

            self.table_rows.append(new_row(self.config, outcome, report))

    def append_skipped(self, report: Any) -> None:
        """Append a new TableRow for the skipped report."""

        if hasattr(report, "wasxfail"):
            outcome = Outcome.XFAILED
        else:
            outcome = Outcome.SKIPPED

        self.table_rows.append(new_row(self.config, outcome, report))

    def pytest_runtest_logreport(self, report: Any) -> None:
        """Append a new TableRow for the current report."""

        if report.passed:
            self.append_passed(report)
        elif report.failed:
            self.append_failed(report)
        elif report.skipped:
            self.append_skipped(report)

    def pytest_sessionfinish(self, session: Any) -> None:
        """Hook implementation that stores test reports in BigQuery."""

        write_rows(
            bigquery.Client(project=self.config.option.project_id),
            self.config.option.results_table,
            self.table_rows,
        )


def pytest_addoption(parser):
    """Hook implementation that adds a custom CLI options."""

    burnham_group = parser.getgroup("burnham")
    burnham_group.addoption(
        "--results-table",
        action="store",
        dest="results_table",
        help="BigQuery table for storing results",
        metavar="TABLE",
        type=str,
        required=False,
        default="burnham_derived.test_results_v1",
    )
    burnham_group.addoption(
        "--log-url",
        action="store",
        dest="log_url",
        help="URL for viewing logs of this task instance in Airflow",
        metavar="URL",
        type=str,
        required=True,
    )


def pytest_configure(config) -> None:
    """Hook implementation that registers the plugin."""

    config.pluginmanager.register(StoreResults(config), "bigquery_store_results")


def pytest_unconfigure(config) -> None:
    """Hook implementation that unregisters the plugin."""

    plugin = config.pluginmanager.get_plugin("bigquery_store_results")

    if plugin is None:
        return

    config.pluginmanager.unregister(plugin)
