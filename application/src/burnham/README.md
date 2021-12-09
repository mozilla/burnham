# Burnham Specifics

## Command Line Flags

* -V, --version
  * Print debug information to the console
* -v, --verbose
  * ID of the current test run
* -r, --test-run
  * Name of the current test
* -n, -test-name
  * Data Platform URL
* -p, --platform
  * Interface for the spore-drive technology
* -s, --spore-drive
  * Interface for the spore-drive technology
* -t, -T, --enable-telemetry, --disable-telemetry
  * Enable/Disable telemetry submission with Glean

## Environment Variables

* BURNHAM_VERBOSE
  * boolean
  * Print debug information to the console
* BURNHAM_TEST_RUN
  * string
  * ID of the current test run
* BURNHAM_TEST_NAME
  * string
  * Name of the current test
* BURNHAM_PLATFORM_URL
  * string
  * Data Platform URL
* BURNHAM_SPORE_DRIVE
  * string
    * options: tardigrade, tardigrade-dna
  * Interface for the spore-drive technology
* BURNHAM_TELEMETRY
  * boolean
  * Enable/Disable telemetry submission with Glean
* BURNHAM_MISSIONS
  * string
    * ex.: MissionA
  * Burnham missions


## Missions

Missions are the main way to use burnham. With Missions you can send pings and Glean Metrics for measuring. 

Lets start with the raw functions that each mission will use. Below you can find their names and a brief explanation.

* `Warp`
  * Metric Type: Labeled Counter
  * Increments the space_travel metric
* `Jump`
  * Metric Type: Labeled Counter
  * Increments the space_travel metric
* `Metric Error`
  * Type: Ping
  * Sends a ping that creates a Glean Validation error.
* `Disable Glean Upload`
  * Disables Glean SDK metrics collection and ping Upload
* `Enable Glean Upload`
  * Enables Glean SDK metrics collection and ping Upload

### Mission List

Burnham includes a variety of missions: 

* Mission A
  * Warp 1 time
* Mission B
  * Warp 2 times
* Mission C
  * Jump 1 time
* Mission D
  * Jump 2 times
* Mission E
  * Jump 1 time, one Metric Error
* Mission F
  * Warp 2 times, Jump 1 time
* Mission G
  * Warp 5 times, Jump 4 times
* Mission H
  * Disable Glean upload
  * Sleeps for 5 seconds and then disable Glean SDK metrics collection and  ping upload
* Mission I
  * Enable Glean Upload
  * Enables Glean SDK metrics collection and ping upload.



## Specifics

Burnham uses 3 main Glean metrics. Note: Some types are used more than once

* [UUID](https://mozilla.github.io/glean/book/reference/metrics/uuid.html)
  * ID of the current test run
* [String](https://mozilla.github.io/glean/book/reference/metrics/string.html)
  * Name of the current test.
  * The identifier of the current mission.
  * The status of the current mission.
* [Labeled Counter](https://mozilla.github.io/glean/book/reference/metrics/labeled_counters.html)
  * Counts the number of times a space-travel technology is used. Ex: Jump or Warp.

The pings burnham sends are as follows:

* discovery
  * Custom ping sent by the burnham CLI app.
* space-ship-ready
  * Custom ping for testing kebab-case ping names.
* starbase64
  * Custom ping for testing ping names that contain numbers.
