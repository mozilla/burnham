# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys

import click
from glean import Glean
from glean.config import Configuration

from burnham import __title__, __version__, metrics
from burnham.exceptions import BurnhamError
from burnham.missions import MissionBase
from burnham.space_travel import Discovery, SporeDrive, WarpDrive


@click.command()
@click.version_option(
    __version__, "-V", "--version",
)
@click.argument("mission_name", envvar="BURNHAM_MISSION", type=str)
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
    "-s",
    "--spore-drive",
    help="Interface for the spore-drive technology",
    type=click.Choice(["tardigrade", "tardigrade-dna"]),
    required=False,
    envvar="BURNHAM_SPORE_DRIVE",
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
    mission_name: str,
    platform: str,
    telemetry: bool,
    test_run: str,
    test_name: str,
    spore_drive: str,
    verbose: bool,
) -> None:
    """Entrypoint for the burnham CLI app."""

    Glean.initialize(
        application_id=__title__,
        application_version=__version__,
        upload_enabled=telemetry,
        configuration=Configuration(server_endpoint=platform, log_pings=verbose),
    )

    metrics.test.burnham.test_run.set(test_run)
    metrics.test.burnham.test_name.set(test_name)

    if mission_name not in MissionBase.missions:
        click.echo(f"Invalid mission name '{mission_name}'.", err=True)
        sys.exit(1)

    try:
        MissionBase.missions[mission_name].start(
            Discovery(
                warp_drive=WarpDrive(),
                spore_drive=SporeDrive(
                    branch=spore_drive, active=spore_drive is not None
                ),
            )
        )
    except BurnhamError as exc:
        click.echo(f"An error has occured: {exc}", err=True)
        sys.exit(1)
