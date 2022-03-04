# burnham

Application for end-to-end testing [Mozilla's Glean telemetry][Glean]. 👩‍🚀

## Development status

We successfully completed the proof of concept and are now running burnham in
production. 🚀

## Community

Please check out the [good first issue][good first issue] label for tasks, that
are good candidates for your first contribution to **burnham**. Your
contributions are greatly appreciated! Every little bit helps, and credit will
always be given! 👍

Please note that **burnham** is released with a [Contributor Code of
Conduct][code of conduct]. By participating in this project you agree to abide
by its terms.

## License

Distributed under the terms of the [Mozilla Public License 2.0][license],
**burnham** is free and open source software.

## Installation

**burnham** is available for download from [PyPI][PyPI] via [pip][pip]:

```text
pip install burnham
```

Versions follow [Calendar Versioning][calver] using a `YY.MINOR.MICRO` scheme. 🗓

🚧 Note that we currently don't automatically upload new releases to PyPI
(see [GitHub issue #57][issue57]).

[issue57]: https://github.com/mozilla/burnham/issues/57

## Usage

```text
burnham [OPTIONS] MISSIONS...
```

The accepted values for `MISSIONS` are the `identifier` values for missions in [missions.py][missions.py]

For example: `"MISSION G: FIVE WARPS, FOUR JUMPS" "MISSION C: ONE JUMP"`

[missions.py]: /application/src/burnham/missions.py

### CLI options

All available CLI options for burnham are defined in [cli.py][cli.py].

Copied here for your convenience. 📋

| Short name | Long name             | Environment variable   | Type  | Description                                                                                   |
| ---------- | --------------------- | ---------------------- | ----- | --------------------------------------------------------------------------------------------- |
|            | `--help`              |                        |       | Print the help message                                                                        |
| `-v`       | `--version`           |                        |       | Print the app's version number to the console                                                 |
| `-r`       | `--test-run`          | `BURNHAM_TEST_RUN`     | `str` | ID of the current test run                                                                    |
| `-n`       | `--test-name`         | `BURNHAM_TEST_NAME`    | `str` | Name of the current test                                                                      |
| `-p`       | `--platform`          | `BURNHAM_PLATFORM_URL` | `str` | Data Platform URL                                                                             |
| `-s`       | `--spore-drive`       | `BURNHAM_SPORE_DRIVE`  | `str` | Interface for the spore-drive technology. Accepted values: `["tardigrade", "tardigrade-dna"]` |
| `--t`      | `--enable-telemetry`  | `BURNHAM_TELEMETRY`    |       | Enable telemetry submission with Glean                                                        |
| `-T`       | `--disable-telemetry` | `BURNHAM_TELEMETRY`    |       | Disable telemetry submission with Glean                                                       |

[cli.py]: /application/src/burnham/cli.py

## Custom Glean SDK distribution

When working on a bug fix for the Python bindings for the Glean SDK, you may
wish to replace the glean-sdk wheel installed in the burnham Docker image
with a custom distribution.

Bump the glean-sdk version identifier before you build a wheel distribution
for the glean-sdk and optionally every dependency of glean-sdk that you added
or upgraded. Be sure to check the `requirements.txt` file for the pinned
dependencies. 📦

Then update the [Dockerfile][dockerfile] to copy the local wheels into the
Docker image:

```text
COPY --from=wheels /wheels/*.whl /tmp/wheels/

# Copy custom distribution to temporary wheels directory in image
COPY glean_sdk-31.2.1-cp36-abi3-manylinux1_x86_64.whl /tmp/wheels/
```

Then make sure that the version requirement for the Python bindings for the
Glean SDK and its dependencies in the [burnham setup.py][setup.py] matches
your custom distributions.

```text
install_requires=["click>=7.0", "glean-sdk==31.2.1", "wrapt", "typing_extensions"]
```

When you build the burnham Docker image you should now see a message that pip
has installed your custom wheels in the log.

## Run burnham missions locally

You can run the `fake-data-platform` and the burnham missions locally using
`docker-compose`. Run the following command from the top-level directory:

```text
docker-compose up --build
```

This will launch the platform and run 3 additional containers running
`burnham`. It will print logs from all containers to stdout, the log of
`platform` should show the received pings. The `burnham` containers will exit
automatically, you can stop the platform with Ctrl-C.

[Glean]: https://mozilla.github.io/glean/book/index.html
[PyPI]: https://pypi.org/project/burnham/
[pip]: https://pypi.org/project/pip/
[good first issue]: https://github.com/mozilla/burnham/labels/good%20first%20issue
[code of conduct]: https://github.com/mozilla/burnham/blob/main/application/CODE_OF_CONDUCT.md
[license]: https://github.com/mozilla/burnham/blob/main/application/LICENSE
[calver]: https://calver.org
[dockerfile]: https://github.com/mozilla/burnham/blob/main/application/Dockerfile
[setup.py]: https://github.com/mozilla/burnham/blob/main/application/setup.py
