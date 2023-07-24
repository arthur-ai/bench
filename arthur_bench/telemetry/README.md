# Telemetry

By default, Arthur is collecting anonymous telemetry data about general usage.

## Data being collected

We track usage data in order to best understand what features users like and use.  Specifically, we collect:
- Scoring method used
- Number of runs per test suite
- Test suite and test run names
- Number of test cases for a test run

An example event looks like (user-id is a random identifier, not tied to any personal data).

```
{
    "event_properties": {
        "num_test_runs_for_suite": 3,
        "scoring_method": {
            "scoring_method": "summary_quality"
        },
        "suite_name": "news_summary"
    },
    "event_type": "test_runs",
    "user_id": "efd39923-9f2a-4ad3-bebb-547b8d2cf14a"
}
```

## Opting-out

To opt-out, set the environment variable BENCH_TELEMETRY_DISABLED=1. To opt-out and instead log events that would have been pushed, set BENCH_TELEMETRY_DISABLED=log.

