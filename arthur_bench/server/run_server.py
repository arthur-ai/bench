import argparse
from pathlib import Path
import os
import json
import uuid


try:
    import duckdb
    import uvicorn
    from fastapi import FastAPI, Request
    from fastapi.responses import HTMLResponse, RedirectResponse
    from fastapi.templating import Jinja2Templates
    from fastapi.staticfiles import StaticFiles

except ImportError as e:
    raise ImportError("Can't run Bench Server without server dependencies, to install run: "
                      "pip install arthur-bench[server]") from e

from arthur_bench.run.utils import _bench_root_dir
from arthur_bench.telemetry.telemetry import send_event, set_track_usage_data

app = FastAPI()
HTML_PATH = Path(__file__).parent / "html"
app.mount("/assets", StaticFiles(directory=HTML_PATH / "assets"), name="assets")

templates = Jinja2Templates(directory=HTML_PATH)


templates = Jinja2Templates(directory=Path(__file__).parent / "html")

SERVER_ROOT_DIR: str
ID_FILE: str = "id.json"
USER_ID: uuid.UUID

TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'


@app.get("/", response_class=RedirectResponse)
def home(request: Request):
    return templates.TemplateResponse("usage_data_prompt.html", {"request": request})

@app.get("/test_suites", response_class=HTMLResponse)
def test_suites(request: Request, usage_data: bool = False):
    set_track_usage_data(USER_ID, usage_data)
    try:
        suites = duckdb.sql(f"SELECT name, description, created_at, scoring_method FROM read_json_auto('{SERVER_ROOT_DIR}/*/suite.json', timestampformat='{TIMESTAMP_FORMAT}')").df().to_dict('records')
    except duckdb.IOException:
        suites = []
    send_event({"event_type": "test_suites", "event_properties": {"num_test_suites": len(suites)}})
    return templates.TemplateResponse("test_suite_overview.html", {"request": request,
                                                                   "suites": suites})


@app.get("/test_suites/{test_suite_name}/runs", response_class=HTMLResponse)
def test_runs(request: Request, test_suite_name: str):
    try:
        runs = duckdb.sql(f"SELECT name, created_at, model_name FROM read_json_auto('{SERVER_ROOT_DIR}/{test_suite_name}/*/run.json',timestampformat='{TIMESTAMP_FORMAT}')").df().to_dict('records')
    except duckdb.IOException:
        runs = []
    send_event({"event_type": "test_runs", "event_properties": {"num_test_runs_for_suite": len(runs)}})
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
    send_event({"event_type": "test_run", "event_properties": {"cases_in_run": len(cases)}})
    return templates.TemplateResponse("test_run_table.html", {"request": request,
                                                              "cases": cases,
                                                              "test_suite_name": test_suite_name,
                                                              "run_name": run_name})

def get_or_persist_id() -> uuid.UUID:
    file_name = os.path.join(SERVER_ROOT_DIR, ID_FILE)
    if os.path.isfile(file_name):
        with open(file_name) as f:
            u = json.loads(f.read())
            return u['id']

    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    id = uuid.uuid4()
    with open(file_name, 'w+') as f:
        f.write(json.dumps({'id': str(id)}))
    return id

def run():
    # parser needs to go in this function for compatibility with packaging
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', required=False, help="optional directory override to run as root for bench server ")
    args = parser.parse_args()

    global SERVER_ROOT_DIR
    SERVER_ROOT_DIR = _bench_root_dir()
    if args.directory:
        SERVER_ROOT_DIR = args.directory

    global USER_ID
    USER_ID = get_or_persist_id()

    uvicorn.run("arthur_bench.server.run_server:app", host="127.0.0.1", port=8000, log_level="info")


if __name__  == '__main__':
   run()