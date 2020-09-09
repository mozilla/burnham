# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
import sys
from typing import Tuple

import click

from burnham import __title__, __version__, metrics
from burnham.exceptions import BurnhamError
from burnham.missions import Mission, complete_mission, missions_by_identifier
from burnham.space_travel import Discovery, SporeDrive, WarpDrive
from glean import Glean
from glean.config import Configuration


class MissionParamType(click.ParamType):
    """Custom Param Type for space-travel missions."""

    def convert(self, value, param, ctx) -> Mission:
        """Look up Mission by its identifier."""
        identifier = click.STRING(value, param, ctx)

        if identifier not in missions_by_identifier:
            raise click.BadParameter(
                f'Unknown mission identifier "{identifier}"', ctx, param,
            )

        return missions_by_identifier[identifier]


@click.command()
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
@click.option(
    "-t/-T",
    "--enable-telemetry/--disable-telemetry",
    help="Enable/Disable telemetry submission with Glean",
    type=bool,
    default=True,
    is_flag=True,
    envvar="BURNHAM_TELEMETRY",
)
@click.argument(
    "missions",
    envvar="BURNHAM_MISSIONS",
    type=MissionParamType(),
    nargs=-1,
    required=True,
)
def burnham(
    verbose: bool,
    test_run: str,
    test_name: str,
    enable_telemetry: bool,
    platform: str,
    spore_drive: str,
    missions: Tuple[Mission],
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
        upload_enabled=enable_telemetry is True,
        configuration=Configuration(server_endpoint=platform),
    )

    metrics.test.run.set(test_run)
    metrics.test.name.set(test_name)

    space_ship = Discovery(
        warp_drive=WarpDrive(),
        spore_drive=SporeDrive(branch=spore_drive, active=spore_drive is not None),
    )

    try:
        for mission in missions:
            complete_mission(space_ship=space_ship, mission=mission)
    except BurnhamError as err:
        click.echo(f"Error: {err}", err=True)
        sys.exit(1)
