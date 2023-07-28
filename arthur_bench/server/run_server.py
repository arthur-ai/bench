import glob
import argparse
from pathlib import Path
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
from arthur_bench.telemetry.config import get_or_persist_id, persist_usage_data
from arthur_bench.models.models import TestSuiteRequest

app = FastAPI()
HTML_PATH = Path(__file__).parent / "html"
app.mount("/assets", StaticFiles(directory=HTML_PATH / "assets"), name="assets")

templates = Jinja2Templates(directory=HTML_PATH)


templates = Jinja2Templates(directory=Path(__file__).parent / "html")

SERVER_ROOT_DIR: Path
USER_ID: uuid.UUID

TIMESTAMP_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'


@app.get("/", response_class=RedirectResponse)
def home(request: Request):
    return RedirectResponse("/test_suites")

@app.get("/test_suites", response_class=HTMLResponse)
def test_suites(request: Request):
    suites = []
    suite_files = glob.glob(f'{SERVER_ROOT_DIR}/*/suite.json')
    print('{SERVER_ROOT_DIR}/*/suite.json')
    for f in suite_files:
        suite_obj = TestSuiteRequest.parse_file(f)
        suites.append(suite_obj.dict())
    
    send_event({"event_type": "test_suites_load", "event_properties": {"num_test_suites_load": len(suites), "test_suites_all": [suite['scoring_method'] for suite in suites]}}, USER_ID)
    return templates.TemplateResponse("test_suite_overview.html", {"request": request,
                                                                   "suites": suites})


@app.get("/test_suites/{test_suite_name}/runs", response_class=HTMLResponse)
def test_runs(request: Request, test_suite_name: str):
    try:
        runs = duckdb.sql(f"SELECT name, created_at, model_name FROM read_json_auto('{SERVER_ROOT_DIR}/{test_suite_name}/*/run.json',timestampformat='{TIMESTAMP_FORMAT}')").df().to_dict('records')
        suite = duckdb.sql(f"SELECT scoring_method FROM read_json_auto('{SERVER_ROOT_DIR}/{test_suite_name}/suite.json', timestampformat='{TIMESTAMP_FORMAT}')").df().to_dict('records')[0]
    except duckdb.IOException:
        runs = []
        suite = "Unknown"
    send_event({"event_type": "test_runs_load", "event_properties": {"test_runs_all": [str(run['created_at']) for run in runs], "scoring_method_real": suite}}, USER_ID)
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

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--enable_push_usage_data', help="Enable sending anonymous usage data", required=False, action='store_true')
    group.add_argument('--disable_push_usage_data', help="Disable sending anonymous usage data", required=False, action='store_true')
    args = parser.parse_args()
    if args.enable_push_usage_data:
        persist_usage_data(True)
        return
    if args.disable_push_usage_data:
        persist_usage_data(False)
        return

    global SERVER_ROOT_DIR
    default_root_dir = _bench_root_dir()
    if args.directory:
        default_root_dir = args.directory
    SERVER_ROOT_DIR = Path(default_root_dir).resolve()

    global USER_ID
    config = get_or_persist_id()
    set_track_usage_data(config)
    USER_ID = config.user_id

    uvicorn.run("arthur_bench.server.run_server:app", host="127.0.0.1", port=8000, log_level="info")


if __name__  == '__main__':
   run()