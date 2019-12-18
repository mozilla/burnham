# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pathlib
import setuptools


def read(*args: str) -> str:
    file_path = pathlib.Path(__file__).parent.joinpath(*args)
    return file_path.read_text("utf-8")


setuptools.setup(
    name="burnham",
    version="0.1.0.dev2",
    author="Raphael Pierzina",
    author_email="raphael@hackebrot.de",
    maintainer="Raphael Pierzina",
    maintainer_email="raphael@hackebrot.de",
    license="MPL 2.0",
    url="https://github.com/hackebrot/burnham",
    project_urls={
        "Repository": "https://github.com/hackebrot/burnham",
        "Issues": "https://github.com/hackebrot/burnham/issues",
    },
    description="Application for end-to-end testing Mozilla's Glean telemetry. 👩‍🚀",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=["click>=7.0"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python",
        "Topic :: Software Development :: Testing",
    ],
    entry_points={"console_scripts": ["burnham = burnham.cli:burnham"]},
    keywords=["testing", "telemetry", "command-line"],
)
