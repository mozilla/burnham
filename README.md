# burnham

The burnham project is a new end-to-end test suite that aims to automatically
verify that Glean-based products correctly measure, collect, and submit
non-personal information to the GCP-based Data Platform and that the received
telemetry data is then correctly processed, stored to the respective tables and
made available in BigQuery. 👩‍🚀📈🤖

## Overview

### glean-sdk

For Mozilla, getting reliable data from our products is critical to inform
our decision making. Glean is our new product analytics & telemetry solution
that provides a consistent experience and behavior across all of our
products.

Find out more in our [Firefox Data Documentation][firefox_data]. 📝

### burnham

We have developed a new command-line application based on the [Glean Python
SDK][glean_python_sdk] for producing test data for this end-to-end test
suite. The burnham application submits Glean pings to the Data Platform which
validates and stores these pings in BigQuery tables. The burnham application
was built to be used in test automation by Mozilla engineers and is **not**
meant to be used by users.

You can find the code for the burnham application in the [application
directory][application]. 👩‍🚀

### burnham-bigquery

We also developed a new test suite based on the [pytest][pytest] framework
that dynamically generates tests. Each test runs a specific query on BigQuery
to verify a certain test scenario.

The test suite code is located in the [bigquery][bigquery] directory. 📊

### telemetry-airflow

We build and push Docker images for both burnham and burnham-bigquery on CI
for pushes to the main branch of this repository. The end-to-end test suite
is configured as a DAG on [telemetry-airflow][telemetry-airflow] on the Data
Platform and scheduled to run daily. It runs several instances of a burnham
Docker container to produce Glean telemetry, uses an Airflow sensor to wait
for the data to be available in the burnham live tables, and then runs
burnham-bigquery to verify the results.

Please see the [burnham DAG][airflow_dag] for more information. 📋

## Development status

This project is under active development. 🚧

## Requirements

Both burnham and burnham-bigquery run on Python 3.7 on Debian.

## Integration points

The burnham project has integration points with the Glean SDK team, the Data
Platform team and the Ecosystem Test Engineering team.

## Community Participation Guidelines

This repository is governed by Mozilla's code of conduct and etiquette. Please
read the burnham [Code of Conduct][code_of_conduct].

[application]: /application
[code_of_conduct]: /CODE_OF_CONDUCT.md
[bigquery]: /bigquery
[airflow_dag]: https://github.com/mozilla/telemetry-airflow/blob/master/dags/burnham.py
[firefox_data]: https://docs.telemetry.mozilla.org/concepts/glean/glean.html
[pytest]: https://pypi.org/project/pytest/
[glean_python_sdk]: https://pypi.org/project/glean-sdk/
[telemetry-airflow]: https://github.com/mozilla/telemetry-airflow
