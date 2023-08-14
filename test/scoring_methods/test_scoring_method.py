import pytest
from typing import List, Optional
from unittest.mock import Mock
from arthur_bench.scoring.scoring_method import ScoringMethod


class MockScorer(ScoringMethod):
    def __init__(self, param_1="default_1", param_2: Optional[str] = None):
        self.param_1 = param_1
        self.param_2 = param_2
        self.param_3 = "param_3"
        self.non_json_param = Mock()
        if param_2 is not None:
            self.modify("test_4")

    def name():
        return "mock"

    def run_batch(
        self,
        candidate_batch: List[str],
        reference_batch: List[str] = None,
        input_text_batch: List[str] = None,
        context_batch: List[str] = None,
    ) -> List[float]:
        pass

    def modify(self, param_4):
        self.param_4 = param_4


@pytest.mark.parametrize(
    "args, expected_dict",
    [
        (
            ["test_1", "test_2"],
            {
                "param_1": "test_1",
                "param_2": "test_2",
                "param_3": "param_3",
                "param_4": "test_4",
            },
        ),
        ([], {"param_1": "default_1", "param_2": None, "param_3": "param_3"}),
    ],
)
def test_scoring_method_to_dict(args, expected_dict):
    scorer = MockScorer(*args)
    assert scorer.to_dict() == expected_dict


def test_scoring_method_from_dict():
    params = {
        "param_1": "test_1",
        "param_2": "test_2",
        "param_3": "param_3",
        "param_4": "test_4",
    }
    scorer = MockScorer.from_dict(params)
    assert scorer.param_1 == "test_1"
    assert scorer.param_2 == "test_2"

    scorer = MockScorer.from_dict({})
    assert scorer.param_1 == "default_1"
    assert scorer.param_2 == None
