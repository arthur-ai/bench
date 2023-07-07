import pathlib
from arthur_bench.run.testsuite import TestSuite
from arthur_bench.run.testrun import TestRun

FIXTURE_FILE_DIR = pathlib.Path(__file__).parent / "fixtures"


def assert_test_suite_equal(test_suite: TestSuite, test_suite_other: TestSuite):
    assert test_suite.suite.name == test_suite_other.suite.name
    assert test_suite.suite.scoring_method == test_suite_other.suite.scoring_method
    assert test_suite.suite.description == test_suite_other.suite.description
    assert test_suite.suite.test_cases == test_suite_other.suite.test_cases


def assert_test_run_equal(test_run: TestRun, test_run_other: TestRun):
    assert test_run.name == test_run_other.name
    assert test_run.test_case_outputs == test_run_other.test_case_outputs
    assert test_run.model_name == test_run_other.model_name
    assert test_run.model_version == test_run_other.model_version
    assert test_run.foundation_model == test_run_other.foundation_model