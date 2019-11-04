"""Fakes for using Glean for Python."""

import pathlib
import typing
import logging
import dataclasses

LOGGER = logging.getLogger("glean")


@dataclasses.dataclass
class LabeledCounter:
    label: str
    current: int = 0

    def record(self, value: int = 1) -> None:
        self.current += value


@dataclasses.dataclass
class SubCategory:
    """Fake for a sub category in metrics.yaml."""

    search_count: typing.Dict[str, LabeledCounter]


@dataclasses.dataclass
class Category:
    """Fake for a category in metrics.yaml."""

    burnham: SubCategory


@dataclasses.dataclass
class Metrics:
    """Fake for a metrics.yaml object."""

    test: Category


def load_metrics(path: pathlib.Path) -> Metrics:
    LOGGER.debug(f"Loading metrics from {path}")
    return Metrics(
        Category(
            SubCategory(
                {
                    label: LabeledCounter(label)
                    for label in ["search_engine1", "search_engine2", "search_engine3"]
                }
            )
        )
    )


@dataclasses.dataclass
class Ping:
    name: str

    def send(self) -> None:
        LOGGER.debug(f"Sending ping {self.name}")


@dataclasses.dataclass
class Pings:
    hello: Ping


def load_pings(path: pathlib.Path) -> Pings:
    LOGGER.debug(f"Loading pings from {path}")
    return Pings(Ping("hello"))
