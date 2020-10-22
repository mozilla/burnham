# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import annotations

import pytest
from glean import Glean, testing


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
