# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import urllib.request
import click


@click.command()
@click.option(
    "-p",
    "--platform",
    help="Data Platform URL",
    type=str,
    required=True,
    envvar="BURNHAM_PLATFORM_URL",
)
@click.argument("path")
def burnham(platform: str, path: str) -> None:
    """Send a GET request to the platform and print the response."""

    with urllib.request.urlopen(f"{platform}/{path}") as response:
        click.echo(response.read())
