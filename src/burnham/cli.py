# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import urllib.request
import click

import glean
import pkg_resources

from . import __version__


@click.command()
@click.version_option(
    __version__, "-V", "--version",
)
@click.option(
    "-p",
    "--platform",
    help="Data Platform URL",
    type=str,
    required=True,
    envvar="BURNHAM_PLATFORM_URL",
)
@click.option(
    "-t",
    "--telemetry",
    help="Enable telemetry recording and submission",
    type=bool,
    default=False,
    is_flag=True,
    envvar="BURNHAM_TELEMETRY",
)
@click.option(
    "-r",
    "--test-run",
    help="ID of the current test run",
    type=str,
    required=True,
    envvar="BURNHAM_TEST_RUN",
)
@click.option(
    "-n",
    "--test-name",
    help="Name of the current test",
    type=str,
    required=True,
    envvar="BURNHAM_TEST_NAME",
)
@click.option(
    "-e",
    "--experiment",
    help="ID of an active experiment",
    type=str,
    required=False,
    envvar="BURNHAM_EXPERIMENT",
)
@click.option(
    "-b",
    "--experiment-branch",
    help="Branch name of an active experiment",
    type=str,
    required=False,
    envvar="BURNHAM_EXPERIMENT_BRANCH",
)
@click.option(
    "-v",
    "--verbose",
    help="Print debug information to the console",
    type=bool,
    default=False,
    is_flag=True,
    envvar="BURNHAM_VERBOSE",
)
def burnham(
    platform: str,
    telemetry: bool,
    test_run: str,
    test_name: str,
    experiment: str,
    experiment_branch: str,
    verbose: bool,
) -> None:
    """Send a GET request to the platform and print the response."""

    click.echo(f"platform: {platform}")
    click.echo(f"telemetry: {telemetry}")
    click.echo(f"test_run: {test_run}")
    click.echo(f"test_name: {test_name}")
    click.echo(f"experiment: {experiment}")
    click.echo(f"experiment-branch: {experiment_branch}")
    click.echo(f"verbose: {verbose}")

    metrics = glean.load_metrics(
        pkg_resources.resource_filename(__name__, "config/metrics.yaml")
    )
    pings = glean.load_pings(
        pkg_resources.resource_filename(__name__, "config/pings.yaml")
    )

    from glean.config import Configuration
    from glean import Glean

    Glean.set_upload_enabled(telemetry)
    Glean.initialize(
        application_id="burnham",
        application_version=__version__,
        configuration=Configuration(server_endpoint=platform, log_pings=verbose),
    )

    if experiment is not None and experiment_branch is not None:
        Glean.set_experiment_active(
            experiment_id=experiment, branch=experiment_branch,
        )

    metrics.test.burnham.test_run.set(test_run)
    metrics.test.burnham.test_name.set(test_name)
    pings.test_start.send()

    metrics.test.burnham.space_travel["warp_drive"].add(4)
    pings.discovery.send()

    pings.test_finish.send()
