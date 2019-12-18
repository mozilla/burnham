# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import click


@click.command()
@click.argument("name")
def burnham(name) -> None:
    """Print a hello message."""
    click.echo(f"Hello {name}! 👩‍🚀")
