# Glean

When you run the [burnham CLI app][cli.py], it will record Glean metrics and
submit Glean pings, if ping upload is enabled (enabled by default). 📊

The program flow for the burnham CLI app is as follows:

1. initialize the Glean SDK by calling `Glean.initialize()`
2. set the `test.run` and `test.name` metrics based on CLI options
3. create a `Discovery` space ship and activate/deactivate experiments
4. submit a `space_ship_ready` ping
5. call `complete_mission()` for every mission passed to the CLI app as an argument
    1. this sets the `mission.identifier` and `mission.status` metrics
    2. this also calls the `complete()` method on each mission
    3. for most missions `complete()` performs a sequence of `space_ship.jump()`
    and `space_ship.warp()` calls, which in turn records to the
    `technology.space_travel` metric
    4. submit a `discovery` ping regardless of wether an error occured or not
6. handle any unexpected errors and set an according exit code
7. wait 5 seconds for telemetry to be sent before terminating the app

## Burnham missions

Burnham missions are defined in [src/burnham/missions.py][missions.py]

As mentioned about for most missions `complete()` performs a sequence of
`space_ship.jump()` and `space_ship.warp()` calls, which in turn records to the
`technology.space_travel` metric.

* `MissionE` is special in that it submits a `starbase46` and then produce
a Glean validation error (stored as a metric in
`metrics.labeled_counter.glean_error_invalid_overflow`)
* `MissionH` is special in that it will disable Glean collection and upload
* `MissionI` is special in that it will enable Glean collection and upload

## Glean metrics

Glean metrics are defined in [src/burnham/config/metrics.yaml][metrics.yaml].

For information about the various Glean metric types see the [Glean Book][metric_types].

## Glean pings

Glean pings are defined in [src/burnham/config/pings.yaml][pings.yaml].

[metrics.yaml]: ../src/burnham/config/metrics.yaml
[pings.yaml]: ../src/burnham/config/pings.yaml
[cli.py]: ../src/burnham/cli.py
[missions.py]: ../src/burnham/missions.py

[metric_types]: https://mozilla.github.io/glean/book/reference/metrics/index.html
