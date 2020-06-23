# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from typing import Iterator


class QueryResult:
    def result(self) -> Iterator:
        return iter([[1, 2, 3, 4], [54, 32, 3, 1]])


class Client:
    def query(self, sql) -> QueryResult:
        return QueryResult()
