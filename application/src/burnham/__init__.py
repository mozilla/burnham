# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

__version__ = "21.0.0"
__title__ = "burnham"
__description__ = "Application for end-to-end testing Mozilla's Glean telemetry. 👩‍🚀"
__url__ = "https://github.com/mozilla/burnham"

__author__ = "Raphael Pierzina"
__email__ = "raphael@hackebrot.de"

__license__ = "MPL 2.0"
__copyright__ = "Copyright (c) 2019 Raphael Pierzina"

from pkg_resources import resource_filename

from glean import load_metrics, load_pings

metrics = load_metrics(resource_filename(__name__, "config/metrics.yaml"))
pings = load_pings(resource_filename(__name__, "config/pings.yaml"))
