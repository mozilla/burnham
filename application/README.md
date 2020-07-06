# burnham

Application for end-to-end testing [Mozilla's Glean telemetry][Glean]. 👩‍🚀

## Development status

This project is under active development. Do not use it in production. 🚧

## Installation

**burnham** is available for download from [PyPI][PyPI] via [pip][pip]:

```text
pip install burnham
```

Versions follow [Calendar Versioning][calver] using a `YY.MINOR.MICRO` scheme. 🗓

## Usage

```text
burnham [OPTIONS] MISSIONS...
```

## Custom Glean SDK distribution

When working on a bug fix for the Python bindings for the Glean SDK, you may
wish to replace the glean-sdk wheel installed in the burnham Docker image
with a custom distribution.

Bump the glean-sdk version identifier before you build a wheel distribution
and then update the [Dockerfile][dockerfile] to copy the wheel into the
Docker image:

```text
COPY --from=wheels /wheels/*.whl /tmp/wheels/

# Copy custom distribution to temporary wheels directory in image
COPY glean_sdk-31.2.1-cp36-abi3-manylinux1_x86_64.whl /tmp/wheels/
```

Then make sure that the version requirement for the Python bindings for the
Glean SDK in [burnham setup.py][setup.py] matches your custom distribution.

```text
install_requires=["click>=7.0", "glean-sdk==31.2.1", "wrapt", "typing_extensions"]
```

When you build the burnham Docker image you should now see a message that pip
installed your custom glean-sdk wheel in the log.

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

[Glean]: https://mozilla.github.io/glean/book/index.html
[PyPI]: https://pypi.org/project/burnham/
[pip]: https://pypi.org/project/pip/
[good first issue]: https://github.com/mozilla/burnham/labels/good%20first%20issue
[code of conduct]: https://github.com/mozilla/burnham/blob/main/application/CODE_OF_CONDUCT.md
[license]: https://github.com/mozilla/burnham/blob/main/application/LICENSE
[calver]: https://calver.org
[dockerfile]: https://github.com/mozilla/burnham/blob/main/application/Dockerfile
[setup.py]: https://github.com/mozilla/burnham/blob/main/application/setup.py
