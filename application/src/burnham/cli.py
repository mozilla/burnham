# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
import sys

import click
from glean import Glean
from glean.config import Configuration

from burnham import __title__, __version__, metrics
from burnham.exceptions import BurnhamError
from burnham.space_travel import Discovery, SporeDrive, WarpDrive


@click.command()
@click.argument("mission_identifier", envvar="BURNHAM_MISSION", type=str)
@click.version_option(
    __version__, "-V", "--version",
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
    "-t",
    "--telemetry",
    help="Enable telemetry recording and submission",
    type=bool,
    default=False,
    is_flag=True,
    envvar="BURNHAM_TELEMETRY",
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
    "-s",
    "--spore-drive",
    help="Interface for the spore-drive technology",
    type=click.Choice(["tardigrade", "tardigrade-dna"]),
    required=False,
    envvar="BURNHAM_SPORE_DRIVE",
)
def burnham(
    mission_identifier: str,
    verbose: bool,
    test_run: str,
    test_name: str,
    telemetry: bool,
    platform: str,
    spore_drive: str,
) -> None:
    """Travel through space and complete missions with the Discovery crew.

    If telemetry is enabled, measure, collect, and submit non-personal
    information to the specified data platform with Glean.
    """

    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    Glean.initialize(
        application_id=__title__,
        application_version=__version__,
        upload_enabled=telemetry,
        configuration=Configuration(server_endpoint=platform, log_pings=verbose),
    )

    metrics.test.run.set(test_run)
    metrics.test.name.set(test_name)

    try:
        space_ship = Discovery(
            warp_drive=WarpDrive(),
            spore_drive=SporeDrive(branch=spore_drive, active=spore_drive is not None),
        )
        space_ship.complete_mission(identifier=mission_identifier)
    except BurnhamError as err:
        click.echo(f"Error: {err}", err=True)
        sys.exit(1)
