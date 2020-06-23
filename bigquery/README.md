# burnham-bigquery

Test framework for verifying [Glean telemetry][Glean] in BigQuery. 👩‍🔬

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
      "query": "<SQL>",
      "want": [
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
      "query": "<SQL>",
      "want": [
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
