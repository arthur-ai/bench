import os
import pytest
import shutil
from unittest import mock
from arthur_bench.run.testsuite import TestSuite


@pytest.fixture
def bench_temp_dir_empty(tmpdir_factory):
    tmpdir = str(tmpdir_factory.mktemp("bench"))
    yield tmpdir
    shutil.rmtree(str(tmpdir))


def test_quickstart(bench_temp_dir_empty):
    with mock.patch.dict(os.environ, {"BENCH_FILE_DIR": bench_temp_dir_empty}):
        suite = TestSuite(
            "bench_quickstart",
            "exact_match",
            input_text_list=[
                "What year was FDR elected?",
                "What is the opposite of down?",
            ],
            reference_output_list=["1932", "up"],
        )
        run = suite.run(
            "quickstart_run",
            candidate_output_list=["1932", "up is the opposite of down"],
        )
