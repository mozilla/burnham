# burnham-bigquery

Test framework for verifying [Glean telemetry][Glean] in Big Query. 👩‍🔬

## Development status

This project is under active development. Do not use it in production. 🚧

## Usage

The framework accepts JSON-encoded test run information:

```json
{
  "identifier": "<TEST RUN ID>",
  "tests": [
    {
      "name": "test_labeled_counter",
      "sql": "<SQL>",
      "rows": [
        [
          1234,
          5678
        ],
        [
          1111,
          2222
        ]
      ]
    },
    {
      "name": "test_metric_error",
      "sql": "<SQL>",
      "rows": [
        [
          "hello",
          "world"
        ],
        [
          "mozilla",
          "burnham"
        ]
      ]
    }
  ]
}
```

[Glean]: https://mozilla.github.io/glean/book/index.html
