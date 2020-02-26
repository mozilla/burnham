# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable, ClassVar, Dict, Type

from glean import Glean
from wrapt import decorator

from burnham.exceptions import ExperimentError


class Active:
    """Descriptor for the active status of an Experiment."""

    def __init__(self) -> None:
        self.values: Dict[Experiment, bool] = defaultdict(bool)

    def __get__(self, experiment: Experiment, experiment_cls: Type[Experiment]) -> bool:
        return self.values[experiment]

    def __set__(self, experiment: Experiment, value: bool) -> None:
        """Called to set the 'active' status on an Experiment.

        This also updates the status in Glean.
        """

        if value is True and self.values[experiment] is False:
            Glean.set_experiment_active(
                experiment_id=experiment.identifier, branch=experiment.branch,
            )

        if value is False and self.values[experiment] is True:
            Glean.set_experiment_inactive(experiment.identifier)

        self.values[experiment] = value

    def __set_name__(self, experiment_cls: Type[Experiment], name: str) -> None:
        self.experiment_cls = experiment_cls
        self.name = name


@decorator
def check_active(wrapped_method: Callable, experiment: Experiment, args, kwargs) -> Any:
    """Check that the experiment is active when calling methods on it."""

    if experiment.active is False:
        raise ExperimentError(f"Experiment '{experiment.identifier}' is inactive.")

    return wrapped_method(*args, **kwargs)


class ExperimentMeta(type):
    """Metaclass that decorates Experiment methods with check_active."""

    def __new__(cls, name, bases, attrs, **kwargs):

        # Add a new Active descriptor to the Experiment
        attrs["active"] = Active()

        # Make sure the following Experiment methods can only
        # be called if the Experiment is activated.
        methods = ["__call__"]

        for attr, value in attrs.items():
            if attr in methods:
                attrs[attr] = check_active(value)

        return super().__new__(cls, name, bases, attrs, **kwargs)


class Experiment(metaclass=ExperimentMeta):
    """Experimental technology used on a SpaceShip."""

    identifier: ClassVar[str]
    branch: str
    active: bool

    def __init__(self, branch: str = "default", active: bool = False) -> None:
        self.branch = branch
        self.active = active
