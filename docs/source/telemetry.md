# Usage Data Collection

By default, Arthur is collecting anonymous usage data.

## Data being collected

We track usage data in order to best understand what features users like and use.  Specifically, we collect:
- Scoring method used
- Number of runs per test suite
- Number of test cases for a test run

An example event looks like (user-id is a random identifier, not tied to any personal data).

```
{
    "event_properties": {
        "num_test_runs_for_suite": 3,
        "scoring_method": {
            "scoring_method": "summary_quality"
        }
    },
    "event_type": "test_runs",
    "user_id": "efd39923-9f2a-4ad3-bebb-547b8d2cf14a"
}
```

## Opting-out

To opt-out, run
```
bench --disable_push_usage_data
```

If you want to opt back in, run
```
 bench --enable_push_usage_data
```

You can also opt-out, by setting the environment variable BENCH_TELEMETRY_DISABLED=1. To opt-out and instead log events that would have been pushed, set BENCH_TELEMETRY_DISABLED=log.

