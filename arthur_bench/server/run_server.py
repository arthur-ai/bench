import argparse
from pathlib import Path

try:
    import duckdb
    import uvicorn
    from fastapi import FastAPI, Request
    from fastapi.responses import HTMLResponse, RedirectResponse
    from fastapi.templating import Jinja2Templates
except ImportError as e:
    raise ImportError("Can't run Bench Server without server dependencies, to install run: "
                      "pip install arthur-bench[server]") from e

from arthur_bench.run.utils import _bench_root_dir

app = FastAPI()

templates = Jinja2Templates(directory=Path(__file__).parent / "html")

SERVER_ROOT_DIR: str

TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'


@app.get("/", response_class=RedirectResponse)
def home(request: Request):
    return RedirectResponse("/test_suites")


@app.get("/test_suites", response_class=HTMLResponse)
def test_suites(request: Request):
    try:
        suites = duckdb.sql(f"SELECT name, description, created_at, scoring_method FROM read_json_auto('{SERVER_ROOT_DIR}/*/suite.json', timestampformat='{TIMESTAMP_FORMAT}')").df().to_dict('records')
    except duckdb.IOException:
        suites = []
    return templates.TemplateResponse("test_suite_overview.html", {"request": request,
                                                                   "suites": suites})


@app.get("/test_suites/{test_suite_name}/runs", response_class=HTMLResponse)
def test_runs(request: Request, test_suite_name: str):
    try:
        runs = duckdb.sql(f"SELECT name, created_at, model_name FROM read_json_auto('{SERVER_ROOT_DIR}/{test_suite_name}/*/run.json',timestampformat='{TIMESTAMP_FORMAT}')").df().to_dict('records')
    except duckdb.IOException:
        runs = []
    return templates.TemplateResponse("test_run_overview.html", {"request": request,
                                                                 "runs": runs,
                                                                 "test_suite_name": test_suite_name})


@app.get("/test_suites/{test_suite_name}/runs/{run_name}", response_class=HTMLResponse)
def test_run_results(request: Request, test_suite_name: str, run_name: str):
    try:
        cases = duckdb.sql(f"SELECT * FROM ("
                        f"SELECT test_cases.input, test_cases.reference_output FROM ("
                        f"SELECT unnest(test_cases) as test_cases from read_json_auto('{SERVER_ROOT_DIR}/{test_suite_name}/suite.json', timestampformat='{TIMESTAMP_FORMAT}'))) "
                        f"POSITIONAL JOIN (SELECT test_cases.output, test_cases.score FROM ("
                        f"SELECT unnest(test_case_outputs) as test_cases from read_json_auto('{SERVER_ROOT_DIR}/{test_suite_name}/{run_name}/run.json',timestampformat='{TIMESTAMP_FORMAT}')))").df().to_dict('records')
    except duckdb.IOException:
        cases = []
    return templates.TemplateResponse("test_run_table.html", {"request": request,
                                                              "cases": cases,
                                                              "test_suite_name": test_suite_name,
                                                              "run_name": run_name})

def run():
    # parser needs to go in this function for compatibility with packaging
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', required=False, help="optional directory override to run as root for bench server ")
    args = parser.parse_args()

    global SERVER_ROOT_DIR 
    SERVER_ROOT_DIR = _bench_root_dir()
    if args.directory:
        SERVER_ROOT_DIR = args.directory
    
    uvicorn.run("arthur_bench.server.run_server:app", host="127.0.0.1", port=8000, log_level="info")


if __name__  == '__main__':
   run()