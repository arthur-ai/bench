## Setup

### Package installation
First [download](https://github.com/arthur-ai/bench/releases) the tar file from the Github releases. Next install the package to your python environment.

Install Bench with optional dependencies for serving results locally (recommended):  
`pip install --find-links=./path_to_tar_file 'arthur-bench[server]'`

Install Bench with minimum dependencies:
`pip install --find-links=./path_to_tar_file 'arthur-bench'`

### Choosing Local vs SaaS:

Bench has two options for tracking datasets and results:

1) Local only (default): save data and run server on the same machine that is running the bench package

2) Arthur SaaS Platform: Use the package client to log data and results to the Arthur platform. Arthur manages data storage and persistence and hosts the bench server.

### Local UI

Bench spins up a local UI (like [tensorboard](https://www.tensorflow.org/tensorboard)) to provide a visual interface for your test data. 

To launch the local UI, run `bench` from the command line. You will see a url for a local server that you can copy and paste into your browser to navigate the UI.

#### Setup

The only setup required is to configure `BENCH_FILE_DIR`, which defaults to `./bench_runs` relative to whichever directory you are running the `bench` command from.

#### Examples

Running these commands will launch the local bench UI to explore two test suites we have prepared as examples on our github repo

```
 # clone the bench repo
git clone git@github.com:arthur-ai/bench.git

# navigate to the examples folder with the test run data
cd bench/examples 

# launch the UI
bench
```

### Arthur SaaS

Bench can be used automatically in conjunction with your team's existing Arthur platform account. If you are using Arthur Bench as a standalone tool without the rest of the Arthur observability platform, you can skip this step.

To connect to the Arthur Platform from Bench, you will need an Arthur Bench account and API key. To obtain an API key, send an email to rowan@arthur.ai.

To log results to the platform, you just need to set the remote url and api key environment variables before creating and running suites. For example,  
```
import os
os.environ['ARTHUR_API_URL'] = 'https://app.arthur.ai'
os.environ['ARTHUR_API_KEY'] = 'FILL ME IN'
```
