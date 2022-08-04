# burnham 👩‍🚀📈🤖

**❌ As of August 4, 2022, the burnham end-to-end test suite was disabled on
Airflow. The source code in this repository is no longer actively maintained and
the repository was marked as read-only as a result. ❌**

The burnham project is an end-to-end test suite that aims to automatically
verify that Glean-based products correctly measure, collect, and submit
non-personal information to the GCP-based Data Platform and that the received
telemetry data is then correctly processed, stored to the respective tables
and made available in BigQuery.

Blog post about the proof of concept:
https://raphael.codes/blog/automated-end-to-end-tests-for-glean/

## Overview

### Glean SDK

For Mozilla, getting reliable data from our products is critical to inform
our decision making. Glean is a product analytics & telemetry solution that
provides a consistent experience and behavior across all of our products.

Find out more in our [Data Documentation][data_documentation]. 📝

### burnham

We have developed a command-line application based on the [Glean SDK Python
bindings][glean_sdk] for producing test data as part of the automated
end-to-end test suite. The burnham application submits Glean pings to the
Data Platform which validates and stores these pings in BigQuery tables.

You can find the code for the burnham application in the [application
directory][application]. 👩‍🚀

### burnham-bigquery

We also developed a test suite based on the [pytest][pytest] framework that
dynamically generates tests. Each test runs a specific query on BigQuery to
verify a certain test scenario. After the test session finished, we then
store the results in a designated BigQuery table with ID
`burnham_derived.test_results_v1`.

The test suite code is located in the [bigquery][bigquery] directory. 📊

### telemetry-airflow

We build and push Docker images for both burnham and burnham-bigquery on CI
for pushes to the `main` branch of this repository. The end-to-end test suite
is configured as a DAG on [telemetry-airflow][telemetry-airflow] on the Data
Platform and scheduled to run daily. It runs several instances of a burnham
Docker container to produce Glean telemetry, uses Airflow sensors to wait for
the data to be available in the various burnham live tables, and then runs
burnham-bigquery to verify the results.

Please see the [burnham DAG][airflow_dag] for more information. 📋

### Redash

We created two scheduled queries that read the results from the
`burnham_derived.test_results_v1` table from the past 4 days. The queries run
daily at 02:00 UTC after telemetry-airflow ran the burnham DAG.

Mozilla employees can find this information in the [burnham
dashboard][redash].

## Development status

We successfully completed the proof of concept and are now running burnham
and burnham-bigquery in production. We are now actively working on developing
additional test scenarios. 🚀

## Requirements

Both burnham and burnham-bigquery run on Python 3.7 on Debian.

## Integration points

The burnham project has integration points with the Glean SDK team, the Data
Platform team and the Ecosystem Test Engineering team.

## Community Participation Guidelines

This repository is governed by Mozilla's code of conduct and etiquette. Please
read the burnham [Code of Conduct][code_of_conduct].

## Project theme

The project theme is inspired by Michael Burnham, the fictional protagonist
on the web television series Star Trek: Discovery portrayed by Sonequa
Martin-Green. Burnham is a science specialist on the Discovery. She and her
crew do research on spore drive technology and complete missions in outer
space and these themes of scientific exploration and space travel are a
perfect fit for this project. 👩‍🚀

[application]: /application
[code_of_conduct]: /CODE_OF_CONDUCT.md
[bigquery]: /bigquery
[airflow_dag]: https://github.com/mozilla/telemetry-airflow/blob/master/dags/burnham.py
[data_documentation]: https://docs.telemetry.mozilla.org/concepts/glean/glean.html
[pytest]: https://pypi.org/project/pytest/
[glean_sdk]: https://pypi.org/project/glean-sdk/
[telemetry-airflow]: https://github.com/mozilla/telemetry-airflow
[redash]: https://sql.telemetry.mozilla.org/dashboard/burnham
