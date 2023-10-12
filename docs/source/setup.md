# Setup

## Package installation

Install Bench to your python environment with optional dependencies for serving results locally (recommended):  

`pip install 'arthur-bench[server]'`

Alternatively, install Bench to your python environment with minimal dependencies:

`pip install arthur-bench`

## Choosing Local vs SaaS:

Bench has two options for tracking datasets and results:

1) Local only (default): save data and run server on the same machine that is running the bench package

2) Arthur SaaS Platform (Coming soon!): Use the package client to log data and results to the Arthur platform. Arthur manages data storage and persistence and hosts the bench server.

## Local

Bench spins up a local UI (like [tensorboard](https://www.tensorflow.org/tensorboard)) to provide a visual interface for your test data.

### View Examples

Running these commands will view launch the bench UI locally to view the example test suites from the Arthur Bench GitHub repo.

```
# clone the bench repo
git clone https://github.com/arthur-ai/bench.git

# set the BENCH_FILE_DIR environment variable to point to the example test suite data in the repo
export BENCH_FILE_DIR="./bench/examples/bench_runs/"

# launch the bench UI
bench
```
You will see a url for a local server that you can copy and paste into your browser to navigate the UI.

Viewing examples in the bench UI will look something like this:
<p align="center">
<img src="./_static/img/Bench_UI_Screenshot.png" alt="Examples UI" width="1100"/>

When you want to view the local UI for your own test suites going forward, make sure your `BENCH_FILE_DIR` environment variable is configured to point to the location of your new test runs, and run `bench` from the command line.

## SaaS (Coming Soon!)

Bench can be used automatically in conjunction with your team's existing Arthur platform account. To connect to the Arthur Platform from Bench, you will need an Arthur Bench account and API key.

To log results to the platform, you just need to set the remote url and api key environment variables before creating and running suites. For example,  
```
import os
os.environ['ARTHUR_BENCH_AUTOLOG'] = 'true'
os.environ['ARTHUR_API_URL'] = 'https://app.arthur.ai'
os.environ['ARTHUR_API_KEY'] = 'FILL ME IN'
```
