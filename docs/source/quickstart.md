## Quickstart
### Package installation and environment setup
Install Bench with minimum dependencies:

`pip install -e .`

Install Bench with optional dependencies for serving results locally:  
`pip install -e '.[server]'`

Bench has two options for tracking datasets and results:

1) Local only: save data and run server on the same machine that is running the bench package

2) Arthur SaaS Platform: Use the package client to log data and results to the Arthur platform. Arthur manages data storage and persistence and hosts the bench server.

#### Running in local mode

Bench saves test suites and test runs to the directory specified by the `BENCH_FILE_DIR`, which defaults to `./bench`

Suites can be viewed in browser by running `bench` from the command line.

#### Logging to your remote Arthur organization

First, create an Arthur Bench account and obtain an API key.

To log results to the platform, you just need to set the remote url and api key environment variables before creating and running suites. For example,  
```
import os
os.environ['ARTHUR_API_URL'] = 'https://app.arthur.ai'
os.environ['ARTHUR_API_KEY'] = 'FILL ME IN'
```

### Creating your first suite

Instantiate a test suite with name, data, and scoring method.

```
from arthur_bench.run.testsuite import TestSuite

suite = TestSuite('my_bench_test', reference_data_path='./path/to/my_data.csv', scoring_method='bertscore')
```

### Running your test suite

Run the suite on a set of candidate generations, specifying run name, and optional model parameters used during generation. This will score each generation using the scoring method specified by the test suite.

```
suite.run('my_bench_run', candidate_data_path='./path/to/my_model_data.csv', model_name='openai_gpt_35', foundation_model='gpt-3.5-turbo', prompt_template='my_custom_prompt')
```

### Viewing suites and run results
To explore your Bench suites and runs in a broswer, run `bench` from the command line. This will spin up a server where you can view your Test Suites and evaluate Runs across different model and prompt configurations.


For a complete walkthrough and more examples, please visit our [key concepts](concepts.md)