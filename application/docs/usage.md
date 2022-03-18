# Usage

```text
burnham [OPTIONS] MISSIONS...
```

The accepted values for `MISSIONS` are the `identifier` values for missions in [src/burnham/missions.py][missions.py]

For example: `"MISSION G: FIVE WARPS, FOUR JUMPS" "MISSION C: ONE JUMP"`

[missions.py]: ../src/burnham/missions.py

### CLI options

All available CLI options for burnham are defined in [src/burnham/cli.py][cli.py].

Copied here for your convenience. 📋

| Short name | Long name             | Environment variable      | Type  | Description                                                                                   |
| ---------- | --------------------- | ------------------------- | ----- | --------------------------------------------------------------------------------------------- |
|            | `--help`              |                           |       | Print the help message                                                                        |
| `-v`       | `--version`           |                           |       | Print the app's version number to the console                                                 |
| `-r`       | `--test-run`          | `BURNHAM_TEST_RUN`        | `str` | ID of the current test run                                                                    |
| `-n`       | `--test-name`         | `BURNHAM_TEST_NAME`       | `str` | Name of the current test                                                                      |
| `-a`       | `--airflow_task_id`   | `BURNHAM_AIRFLOW_TASK_ID` | `str` | ID of the Airflow task that runs the client                                                   |
| `-p`       | `--platform`          | `BURNHAM_PLATFORM_URL`    | `str` | Data Platform URL                                                                             |
| `-s`       | `--spore-drive`       | `BURNHAM_SPORE_DRIVE`     | `str` | Interface for the spore-drive technology. Accepted values: `["tardigrade", "tardigrade-dna"]` |
| `-t`       | `--enable-telemetry`  | `BURNHAM_TELEMETRY`       |       | Enable telemetry submission with Glean                                                        |
| `-T`       | `--disable-telemetry` | `BURNHAM_TELEMETRY`       |       | Disable telemetry submission with Glean                                                       |

[cli.py]: ../src/burnham/cli.py
