# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from typing import Any, List

from google.cloud.bigquery import Client


def test_burnham(bq_client: Client, query: str, want: List[Any]):
    """Test that the Glean telemetry in BigQuery matches what we expect."""

    job = bq_client.query(query)
    got = [row for row in job.result()]

    assert got == want
