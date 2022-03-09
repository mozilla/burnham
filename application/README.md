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

Please see [docs/usage.md][docs_usage] for information about how to use the burnham application. 🚀

[docs_usage]: ./docs/usage.md

## Development

Please see [docs/development.md][docs_development] for information about Glean metrics
and pings in burnham. 📊

[docs_development]: ./docs/development.md

[Glean]: https://mozilla.github.io/glean/book/index.html
[PyPI]: https://pypi.org/project/burnham/
[pip]: https://pypi.org/project/pip/
[good first issue]: https://github.com/mozilla/burnham/labels/good%20first%20issue
[code of conduct]: https://github.com/mozilla/burnham/blob/main/application/CODE_OF_CONDUCT.md
[license]: https://github.com/mozilla/burnham/blob/main/application/LICENSE
[calver]: https://calver.org
[setup.py]: https://github.com/mozilla/burnham/blob/main/application/setup.py
