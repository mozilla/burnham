# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from typing import Any, List

from google.cloud.bigquery import Client


def test_burnham(bq_client: Client, sql: str, rows: List[Any]):
    """Test that the Glean telemetry in BigQuery matches what we expect."""

    bq_job = bq_client.query(sql)
    bq_rows = [row for row in bq_job.result()]

    assert bq_rows == rows
