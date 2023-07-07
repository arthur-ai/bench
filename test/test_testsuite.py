import os
import pytest
import pandas as pd
import tempfile
from unittest import mock
from typing import List, Optional

from helpers import assert_test_suite_equal, assert_test_run_equal
from arthur_bench.run.testsuite import TestSuite
from arthur_bench.scoring import ScoringMethod
from arthur_bench.run.testrun import TestRun


@pytest.fixture(scope="session")
def mock_reference_data():
    return pd.DataFrame(
        {
            "input": [
                "Mr and Mrs Dursley, of number four, Privet Drive, were proud to say that they were perfectly normal,"
                " thank you very much.",
                "They were the last people you’d expect to be involved in anything strange or mysterious, "
                "because they just didn’t hold with such nonsense",
                "Mr Dursley was the director of a firm called Grunnings, which made drills. "
                "He was a big, beefy man with hardly any neck, although he did have a very large moustache"
            ],
            "reference_output": [
                "Mrs Dursley was thin and blonde and had nearly twice the usual amount of neck, which came in very useful "
                "as she spent so much of her time craning over garden fences, spying on the neighbours",
                "The Dursleys had a small son called Dudley and in their opinion there was no finer boy anywhere. ",
                "The Dursleys had everything they wanted, but they also had a secret, "
                "and their greatest fear was that somebody would discover it"
            ]
        }
    )

@pytest.fixture
def mock_input_strings():
    return [
        "Mr and Mrs Dursley, of number four, Privet Drive, were proud to say that they were perfectly normal,"
        " thank you very much.",
        "They were the last people you’d expect to be involved in anything strange or mysterious, "
        "because they just didn’t hold with such nonsense",
        "Mr Dursley was the director of a firm called Grunnings, which made drills. "
        "He was a big, beefy man with hardly any neck, although he did have a very large moustache"
    ]

@pytest.fixture
def mock_reference_strings():
    return [
        "Mrs Dursley was thin and blonde and had nearly twice the usual amount of neck, which came in very useful "
        "as she spent so much of her time craning over garden fences, spying on the neighbours",
        "The Dursleys had a small son called Dudley and in their opinion there was no finer boy anywhere. ",
        "The Dursleys had everything they wanted, but they also had a secret, "
        "and their greatest fear was that somebody would discover it"
    ]


@pytest.fixture(scope="session")
def mock_outputs():
    return [
        'this is a test run output',
        'this is a good test run output',
        'this is a another test run output'
    ]


@pytest.fixture(scope="session")
def custom_reference_data(mock_reference_data):
    return mock_reference_data.rename(columns={"input": "custom_prompt", "reference_output": "custom_reference"})

@pytest.fixture(scope="session")
def bench_temp_dir(tmpdir_factory):
    tmpdir = str(tmpdir_factory.mktemp("bench"))
    return tmpdir



@pytest.fixture(scope="session")
def test_suite_default(mock_reference_data, bench_temp_dir):
    with mock.patch.dict(os.environ, {"BENCH_FILE_DIR": bench_temp_dir}):
        return TestSuite(
            name="test_suite",
            scoring_method="bertscore",
            reference_data=mock_reference_data
        )


@pytest.fixture(scope="session")
def test_suite_custom(custom_reference_data, bench_temp_dir):
    with mock.patch.dict(os.environ, {"BENCH_FILE_DIR": bench_temp_dir}):
        return TestSuite(
            name="test_suite_custom",
            scoring_method="bertscore",
            reference_data=custom_reference_data,
            description="test_description",
            input_column="custom_prompt",
            reference_column="custom_reference"
        )

@pytest.fixture
def test_suite_string(mock_input_strings, mock_reference_strings, bench_temp_dir):
    with mock.patch.dict(os.environ, {"BENCH_FILE_DIR": bench_temp_dir}):
        return TestSuite(
            name = "test_suite_strings", 
            scoring_method = "bertscore", 
            input_text_list = mock_input_strings, 
            reference_output_list = mock_reference_strings
        ) 


class MockScoringMethod(ScoringMethod):
    def run_batch(self, reference_batch: List[str], candidate_batch: List[str],
                  input_text_batch: Optional[List[str]] = None, context_batch: Optional[List[str]] = None) -> List[float]:
        return [0.8 for _ in range(len(reference_batch))]


@pytest.fixture
def mock_load_scoring():
    def load_scoring_method(name):
        return MockScoringMethod()
    return load_scoring_method


@pytest.mark.parametrize('params,expected', [
    ({"name": "test_suite", "scoring_method": "bertscore", "reference_data": "mock_reference_data"}, "test_suite_default"),
    ({"name": "test_suite_custom", "scoring_method": "bertscore", "description": "test_description",
      "reference_data": "custom_reference_data", "input_column": "custom_prompt", "reference_column": "custom_reference"},
     "test_suite_custom"),
    ({"name": "test_suite_strings", "scoring_method": "bertscore", "input_text_list": "mock_input_strings", 
    "reference_output_list": "mock_reference_strings"}, "test_suite_string")
], ids=['test-suite-default-columns', 'test-suite-custom-columns', 'test-suite-string-no-context'])
def test_create_test_suite(params, expected, request):
    if "reference_data"  in params:
        params["reference_data"] = request.getfixturevalue(params["reference_data"])
    if "input_text_list" in params:
        params["input_text_list"] = request.getfixturevalue(params["input_text_list"])
    if "reference_output_list" in params:
        params["reference_output_list"] = request.getfixturevalue(params["reference_output_list"])

    with tempfile.TemporaryDirectory() as tmpdir:
        with mock.patch.dict(os.environ, {"BENCH_FILE_DIR": tmpdir}):
            suite = TestSuite(**params)
            expected_suite = request.getfixturevalue(expected)
            assert_test_suite_equal(suite, expected_suite)


@pytest.mark.parametrize('candidate_column', ['custom_candidate', None])
def test_run_test_suite(candidate_column, mock_load_scoring, mock_outputs, test_suite_default, bench_temp_dir, mock_test_run):
       with mock.patch.dict(os.environ, {"BENCH_FILE_DIR": bench_temp_dir}):
            with mock.patch('arthur_bench.run.testsuite.load_scoring_method', mock_load_scoring):
                if candidate_column:
                    run = test_suite_default.run(run_name="test_run",
                                                candidate_data=pd.DataFrame({candidate_column: mock_outputs}),
                                                candidate_column=candidate_column,
                                                model_name="my_very_special_gpt",
                                                save=False)

                else:
                    run = test_suite_default.run(run_name="test_run",
                                                candidate_data=pd.DataFrame({"candidate_output": mock_outputs}),
                                                model_name="my_very_special_gpt",
                                                save=False)

                assert_test_run_equal(run, mock_test_run)


@pytest.mark.parametrize('params', [
    {},
    {"input_column": "missing_prompt", "reference_data": pd.DataFrame({"prompt": [], "reference": []})},
    {"reference_column": "missing_reference", "reference_data": pd.DataFrame({"prompt": [], "reference": []})}
], ids=['missing-req-params', 'input-missing', 'reference-missing'])
def test_create_test_suite_invalid(params):
    params.update({"name": "test_suite", "scoring_method": "bertscore"})
    with pytest.raises(ValueError):
        _ = TestSuite(**params)


@pytest.mark.parametrize('params', [
    {"candidate_column": "missing_candidate", "candidate_data":
        pd.DataFrame({"candidate_output": ["three", "outputs", "provided"]})},
    {"candidate_data": pd.DataFrame({"candidate_output": ["only two", "outputs provided"]})}
], ids=['missing-candidate', 'invalid-length'])
def test_run_test_suite_invalid(params, test_suite_default):
    params.update({"run_name": "test_run"})
    with pytest.raises(ValueError):
        _ = test_suite_default.run(**params)
