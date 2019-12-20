# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# See https://flask.palletsprojects.com/en/1.1.x/patterns/singlepageapplications/

import typing
import flask


app = flask.Flask(__name__)


@app.route("/heartbeat")
def heartbeat() -> typing.Any:
    """Return a status response."""
    return flask.jsonify({"status": "healthy"})


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path: str) -> str:
    """Return a response with the requested path."""
    return f"path: '{path}'"
