# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from typing import Any, List

from google.cloud import bigquery


def test_burnham(
    client: bigquery.Client,
    query_job_config: bigquery.QueryJobConfig,
    query: str,
    want: List[Any],
):
    """Test that the Glean telemetry in BigQuery matches what we expect."""
    query_job = client.query(query, job_config=query_job_config)
    got = [dict(row.items()) for row in query_job.result()]
    assert got == want
