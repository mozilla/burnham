# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import shlex
import typing

import pytest
from click.testing import CliRunner

from burnham.cli import burnham


@pytest.fixture(name="run_cli")
def fixture_run_cli() -> typing.Callable:
    """Return a function that invokes a click CLI runner."""

    runner = CliRunner()

    def run(cli_options: str) -> typing.Any:
        """Run the CLI with the given options and return the result."""
        return runner.invoke(burnham, shlex.split(cli_options))

    return run


def test_help(run_cli: typing.Callable) -> None:
    """Test for the help option."""
    result = run_cli("--help")
    assert result.exit_code == 0
    assert "Usage: burnham" in result.output


@pytest.mark.parametrize("option", ["-V", "--version"])
def test_version(run_cli: typing.Callable, option: str) -> None:
    """Test for the version options."""
    result = run_cli(option)
    assert result.exit_code == 0
    assert "burnham, version" in result.output
