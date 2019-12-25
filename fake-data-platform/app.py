# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import typing
import flask
import logging


app = flask.Flask(__name__)
app.logger.setLevel(logging.DEBUG)


@app.route("/heartbeat")
def heartbeat() -> typing.Any:
    """Return a status response."""
    return flask.jsonify({"status": "healthy"})


@app.route("/submit/<app_id>/<ping_name>/<schema_version>/<doc_id>", methods=["POST"])
def glean_ping(
    app_id: str, ping_name: str, schema_version: str, doc_id: str
) -> typing.Any:
    """Endpoint for submitting glean pings."""

    app.logger.debug(flask.request.data)

    return flask.jsonify(
        {
            "app_id": app_id,
            "ping_name": ping_name,
            "schema_version": schema_version,
            "doc_id": doc_id,
        }
    )
